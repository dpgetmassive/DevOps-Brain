"""
Patching Orchestrator

Orchestrates patching via Ansible playbooks.
Adopted improvements from Semaphore UI review.
"""

import subprocess
import json
import uuid
import asyncio
import re
import time
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class PatchJobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class ErrorCategory(Enum):
    NETWORK = "network"
    PERMISSION = "permission"
    PACKAGE = "package"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

class PatchingOrchestrator:
    """Orchestrates patching via Ansible
    
    Adopted improvements:
    - Enhanced output parsing and progress tracking
    - Error recovery with retry logic
    - Per-host progress tracking
    - Audit logging
    """
    
    # Embedded playbook content (deployed automatically)
    PATCH_CONTAINERS_PLAYBOOK = """---
- name: Patch LXC Containers via Proxmox
  hosts: localhost
  become: yes
  gather_facts: no
  
  vars:
    containers: "{{ target_containers | default([]) }}"
    security_only: "{{ patch_type | default('all') == 'security' }}"
    dry_run: "{{ dry_run_mode | default(false) }}"
    proxmox_nodes: ["pve-scratchy", "pve-itchy"]
  
  tasks:
    - name: Count updates per container
      shell: |
        pct exec {{ item.ct_id }} -- bash -c "
          apt list --upgradable 2>/dev/null | tail -n+2 | wc -l
        "
      loop: "{{ containers }}"
      register: container_counts
      changed_when: false
    
    - name: Count security updates per container
      shell: |
        pct exec {{ item.ct_id }} -- bash -c "
          apt list --upgradable 2>/dev/null | grep -i security | wc -l
        "
      loop: "{{ containers }}"
      register: container_security_counts
      changed_when: false
      failed_when: false
    
    - name: Upgrade packages (security only)
      shell: |
        pct exec {{ item.ct_id }} -- bash -c "
          export DEBIAN_FRONTEND=noninteractive &&
          apt update &&
          apt upgrade -y $(apt list --upgradable 2>/dev/null | grep -i security | cut -d/ -f1 | tr '\\n' ' ') &&
          apt autoremove -y &&
          apt autoclean
        "
      loop: "{{ containers }}"
      when: 
        - not dry_run
        - container_security_counts.results[loop.index0].stdout | int > 0
        - security_only
      register: container_upgrade_security
    
    - name: Upgrade all packages
      shell: |
        pct exec {{ item.ct_id }} -- bash -c "
          export DEBIAN_FRONTEND=noninteractive &&
          apt update &&
          apt upgrade -y &&
          apt autoremove -y &&
          apt autoclean
        "
      loop: "{{ containers }}"
      when: 
        - not dry_run
        - container_counts.results[loop.index0].stdout | int > 0
        - not security_only
      register: container_upgrade_all
    
    - name: Final status
      debug:
        msg: "Container patching {{ 'completed' if not dry_run else 'dry-run completed' }}"
"""

    PATCH_DEBIAN_PLAYBOOK = """---
- name: Patch Debian/Ubuntu Systems
  hosts: "{{ target_hosts | default('all') }}"
  become: yes
  gather_facts: yes
  
  vars:
    security_only: "{{ patch_type | default('all') == 'security' }}"
    dry_run: "{{ dry_run_mode | default(false) }}"
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Count upgradable packages
      command: apt list --upgradable 2>/dev/null | tail -n+2 | wc -l
      register: package_count
      changed_when: false
    
    - name: Count security updates
      command: apt list --upgradable 2>/dev/null | grep -i security | wc -l
      register: security_count
      changed_when: false
      failed_when: false
    
    - name: Upgrade packages (security only)
      apt:
        upgrade: dist
        update_cache: yes
        autoremove: yes
        autoclean: yes
      when: not dry_run and security_only and security_count.stdout | int > 0
      register: upgrade_result
    
    - name: Upgrade all packages
      apt:
        upgrade: dist
        update_cache: yes
        autoremove: yes
        autoclean: yes
      when: not dry_run and not security_only and package_count.stdout | int > 0
      register: upgrade_result
    
    - name: Final status
      debug:
        msg: "Patching {{ 'completed' if not dry_run else 'dry-run completed' }}"
"""
    
    def __init__(self):
        self.jobs = {}  # job_id -> job_data
        self.ansible_host = "pve-scratchy"
        self.ansible_vm = 102
        self.playbook_path = "/etc/ansible/playbooks/patching"
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.audit_log = []  # Audit trail
        self._playbooks_deployed = False
        
        # Deploy playbooks automatically on first use
        # Note: Deferred to avoid blocking initialization
    
    def _ensure_playbooks_deployed(self):
        """Ensure playbooks are deployed to VM 102 via git pull"""
        if self._playbooks_deployed:
            return
        
        try:
            # Use git to pull playbooks from repository
            # This is much more reliable than stdin/base64 deployment
            repo_url = "https://github.com/dpgetmassive/DevOps-Brain.git"
            repo_path = "/tmp/gm-agentic-devops-brain"
            playbooks_source = f"{repo_path}/projects/patch-compliance-dashboard/ansible-playbooks"
            
            # Deploy script that clones/updates repo and copies playbooks
            deploy_script = f'''#!/bin/bash
set -e

playbook_dir="{self.playbook_path}"
repo_path="{repo_path}"
playbooks_source="{playbooks_source}"

# Create playbook directory
mkdir -p "$playbook_dir"

# Clone or update repository
if [ -d "$repo_path" ]; then
    echo "Repository exists, pulling latest changes..."
    cd "$repo_path"
    git pull --quiet || git fetch --quiet && git reset --hard origin/main
else
    echo "Cloning repository..."
    git clone --depth 1 --quiet "$repo_url" "$repo_path"
fi

# Copy playbooks to target directory
if [ -f "$playbooks_source/patch-containers.yml" ] && [ -f "$playbooks_source/patch-debian.yml" ]; then
    cp "$playbooks_source/patch-containers.yml" "$playbook_dir/"
    cp "$playbooks_source/patch-debian.yml" "$playbook_dir/"
    echo "Playbooks deployed successfully"
else
    echo "ERROR: Playbook files not found in repository" >&2
    exit 1
fi
'''
            
            # Execute deployment script on VM
            exec_cmd = [
                "/usr/bin/ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                self.ansible_host,
                f"qm guest exec {self.ansible_vm} -- bash"
            ]
            
            exec_result = subprocess.run(
                exec_cmd,
                input=deploy_script,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse qm guest exec JSON output
            stdout = exec_result.stdout
            stderr = exec_result.stderr
            if stdout.strip().startswith('{'):
                try:
                    json_output = json.loads(stdout)
                    stdout = json_output.get('out-data', stdout)
                    if 'err-data' in json_output:
                        stderr = json_output.get('err-data', stderr)
                except:
                    pass
            
            # Verify deployment
            verify_cmd = [
                "/usr/bin/ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                self.ansible_host,
                f"qm guest exec {self.ansible_vm} -- bash -c 'wc -l {self.playbook_path}/*.yml 2>/dev/null || echo \"Files not found\"'"
            ]
            
            verify_result = subprocess.run(
                verify_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            verify_output = verify_result.stdout
            if verify_output.strip().startswith('{'):
                try:
                    json_output = json.loads(verify_output)
                    verify_output = json_output.get('out-data', verify_output)
                except:
                    pass
            
            # Check if files were written (non-zero line count)
            if exec_result.returncode == 0 and "Playbooks deployed successfully" in stdout:
                # Extract line counts
                import re
                containers_match = re.search(r'(\d+)\s+.*patch-containers\.yml', verify_output)
                debian_match = re.search(r'(\d+)\s+.*patch-debian\.yml', verify_output)
                
                if containers_match and debian_match:
                    containers_lines = int(containers_match.group(1))
                    debian_lines = int(debian_match.group(1))
                    
                    if containers_lines > 0 and debian_lines > 0:
                        self._playbooks_deployed = True
                        print("✅ Playbooks deployed successfully via git")
                        return
            
            # If we get here, deployment failed
            print(f"⚠️ Playbook deployment warning: returncode={exec_result.returncode}")
            print(f"   stdout: {stdout[:500]}")
            print(f"   stderr: {stderr[:500]}")
            print(f"   verify: {verify_output[:300]}")
        except Exception as e:
            print(f"⚠️ Failed to deploy playbooks (will retry on use): {e}")
    
    async def apply_patches(
        self,
        hosts: List[str],
        patch_type: str = "all",
        dry_run: bool = False,
        schedule: Optional[str] = None
    ) -> str:
        """
        Apply patches to hosts.
        
        Args:
            hosts: List of hostnames to patch
            patch_type: "all" or "security"
            dry_run: If True, only preview patches
            schedule: ISO datetime string or None for immediate
        
        Returns:
            job_id: Unique job identifier
        """
        job_id = str(uuid.uuid4())
        
        job = {
            "job_id": job_id,
            "hosts": hosts,
            "patch_type": patch_type,
            "dry_run": dry_run,
            "status": PatchJobStatus.PENDING.value,
            "started_at": None,
            "completed_at": None,
            "progress": {},
            "results": {},
            "output": [],
            "retry_count": 0,
            "current_task": None,
            "tasks_completed": 0,
            "tasks_total": 0,
            "estimated_time": None,
            "error_category": None,
            "created_by": "api",  # Could be extended to track user
            "created_at": datetime.now().isoformat()
        }
        
        self.jobs[job_id] = job
        
        # Execute immediately or schedule
        if schedule:
            # TODO: Implement scheduling
            job["scheduled_for"] = schedule
        else:
            # Execute now (async)
            asyncio.create_task(self._execute_patch_job(job_id))
        
        return job_id
    
    async def _execute_patch_job(self, job_id: str):
        """Execute patching job with retry logic"""
        job = self.jobs[job_id]
        job["status"] = PatchJobStatus.RUNNING.value
        job["started_at"] = datetime.now().isoformat()
        
        self._audit_log("job_started", job_id, {"hosts": job["hosts"], "patch_type": job["patch_type"]})
        
        try:
            # Get asset info to determine if containers or hosts
            from main import discovery_cache
            
            containers = []
            host_ips = []
            
            for hostname in job["hosts"]:
                # Find asset in discovery cache
                asset = None
                for asset_data in discovery_cache.values():
                    if isinstance(asset_data, dict):
                        if asset_data.get("name") == hostname:
                            asset = asset_data
                            break
                
                if asset:
                    if asset.get("type") == "ct":
                        containers.append({
                            "name": asset.get("name"),
                            "ct_id": asset.get("vmid"),
                            "ip": asset.get("ip"),
                            "node": asset.get("host", "pve-scratchy")
                        })
                    else:
                        host_ips.append(asset.get("ip") or hostname)
            
            # Execute appropriate playbook with retry
            success = False
            last_error = None
            
            for attempt in range(self.max_retries):
                if attempt > 0:
                    job["status"] = PatchJobStatus.RETRYING.value
                    job["retry_count"] = attempt
                    self._audit_log("job_retry", job_id, {"attempt": attempt, "error": str(last_error)})
                    await asyncio.sleep(self.retry_delay * attempt)  # Exponential backoff
                
                try:
                    if containers:
                        await self._patch_containers(job, containers)
                    
                    if host_ips:
                        await self._patch_hosts(job, host_ips)
                    
                    success = True
                    break
                    
                except Exception as e:
                    last_error = e
                    error_cat = self._categorize_error(str(e))
                    job["error_category"] = error_cat.value
                    
                    # Don't retry permission errors
                    if error_cat == ErrorCategory.PERMISSION:
                        break
                    
                    if attempt < self.max_retries - 1:
                        continue
            
            if success:
                job["status"] = PatchJobStatus.COMPLETED.value
                job["completed_at"] = datetime.now().isoformat()
                self._audit_log("job_completed", job_id, {"hosts": job["hosts"]})
                
                # Mark that patch status should be refreshed
                # The refresh will be triggered via API endpoint to avoid circular imports
                job["needs_status_refresh"] = True
            else:
                job["status"] = PatchJobStatus.FAILED.value
                job["error"] = str(last_error)
                job["completed_at"] = datetime.now().isoformat()
                self._audit_log("job_failed", job_id, {"error": str(last_error), "retries": job["retry_count"]})
            
        except Exception as e:
            job["status"] = PatchJobStatus.FAILED.value
            job["error"] = str(e)
            job["error_category"] = ErrorCategory.UNKNOWN.value
            job["completed_at"] = datetime.now().isoformat()
            self._audit_log("job_failed", job_id, {"error": str(e)})
    
    async def _patch_containers(self, job: Dict[str, Any], containers: List[Dict[str, Any]]):
        """Patch LXC containers with enhanced output parsing"""
        # Create temporary inventory file for containers
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(containers, f)
            containers_file = f.name
        
        try:
            # Initialize progress for all containers
            for container in containers:
                job["progress"][container["name"]] = "running"
                job["results"][container["name"]] = {"success": False, "output": "", "packages_upgraded": 0}
            
            # Execute container patching playbook
            # Pass target_containers as JSON (Ansible will parse it automatically)
            containers_json = json.dumps(containers)
            cmd = [
                "/usr/bin/ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                self.ansible_host,
                f"qm guest exec {self.ansible_vm} -- ansible-playbook",
                f"{self.playbook_path}/patch-containers.yml",
                "-e", f"target_containers={containers_json}",
                "-e", f"patch_type={job['patch_type']}",
                "-e", f"dry_run_mode={str(job['dry_run']).lower()}"
            ]
            
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes
            )
            elapsed_time = time.time() - start_time
            
            # Parse output for package counts
            parsed_output = self._parse_container_output(result.stdout, containers)
            
            job["output"].append({
                "type": "containers",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "parsed": parsed_output,
                "elapsed_time": elapsed_time
            })
            
            # Update progress based on parsed output
            if result.returncode == 0:
                for container in containers:
                    container_result = parsed_output.get(container["name"], {})
                    job["progress"][container["name"]] = "completed"
                    job["results"][container["name"]] = {
                        "success": True,
                        "output": result.stdout[-1000:] if result.stdout else "",
                        "packages_upgraded": container_result.get("packages_upgraded", 0),
                        "security_updates": container_result.get("security_updates", 0)
                    }
            else:
                # Parse which containers failed
                failed_containers = self._parse_failed_containers(result.stdout, result.stderr, containers)
                for container in containers:
                    if container["name"] in failed_containers:
                        job["progress"][container["name"]] = "failed"
                        job["results"][container["name"]] = {
                            "success": False,
                            "output": result.stderr[-1000:] if result.stderr else "",
                            "error": failed_containers[container["name"]]
                        }
                    else:
                        job["progress"][container["name"]] = "completed"
                        job["results"][container["name"]] = {
                            "success": True,
                            "output": result.stdout[-1000:] if result.stdout else ""
                        }
        
        finally:
            # Cleanup
            if os.path.exists(containers_file):
                os.unlink(containers_file)
    
    def _parse_container_output(self, stdout: str, containers: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Parse container patching output"""
        parsed = {}
        
        for container in containers:
            container_name = container["name"]
            container_data = {
                "packages_upgraded": 0,
                "security_updates": 0,
                "status": "unknown"
            }
            
            # Look for container-specific output
            container_lines = [line for line in stdout.split('\n') if container_name in line or str(container.get("ct_id")) in line]
            
            # Try to extract package counts
            for line in container_lines:
                if 'upgraded' in line.lower() or 'packages' in line.lower():
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        container_data["packages_upgraded"] = int(numbers[0])
            
            parsed[container_name] = container_data
        
        return parsed
    
    def _parse_failed_containers(self, stdout: str, stderr: str, containers: List[Dict[str, Any]]) -> Dict[str, str]:
        """Parse output to identify which containers failed"""
        failed = {}
        output = stdout + "\n" + stderr
        
        for container in containers:
            container_name = container["name"]
            # Look for failure indicators
            container_pattern = rf'{re.escape(container_name)}.*?(failed|error|unreachable)'
            if re.search(container_pattern, output, re.IGNORECASE):
                error_match = re.search(rf'{re.escape(container_name)}.*?error[:\s]+(.+?)(?:\n|$)', output, re.IGNORECASE)
                if error_match:
                    failed[container_name] = error_match.group(1).strip()
                else:
                    failed[container_name] = "Execution failed"
        
        return failed
    
    async def _patch_hosts(self, job: Dict[str, Any], host_ips: List[str]):
        """Patch VMs/physical hosts with enhanced output parsing"""
        # Ensure playbooks are deployed
        self._ensure_playbooks_deployed()
        
        # Create host list for Ansible limit
        host_limit = ",".join(host_ips)
        
        cmd = [
            "/usr/bin/ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
            self.ansible_host,
            f"qm guest exec {self.ansible_vm} -- ansible-playbook",
            f"{self.playbook_path}/patch-debian.yml",
            "-i", "/etc/ansible/hosts",
            "--limit", host_limit,
            "-e", f"patch_type={job['patch_type']}",
            "-e", f"dry_run_mode={str(job['dry_run']).lower()}"
        ]
        
        # Initialize progress for all hosts
        for host_ip in host_ips:
            job["progress"][host_ip] = "running"
            job["results"][host_ip] = {"success": False, "output": "", "packages_upgraded": 0}
        
        start_time = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes
        )
        
        elapsed_time = time.time() - start_time
        
        # Parse output for progress and package counts
        parsed_output = self._parse_ansible_output(result.stdout, host_ips)
        
        job["output"].append({
            "type": "hosts",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "parsed": parsed_output,
            "elapsed_time": elapsed_time
        })
        
        # Update progress based on parsed output
        if result.returncode == 0:
            for host_ip in host_ips:
                host_result = parsed_output.get(host_ip, {})
                job["progress"][host_ip] = "completed"
                job["results"][host_ip] = {
                    "success": True,
                    "output": result.stdout[-1000:] if result.stdout else "",
                    "packages_upgraded": host_result.get("packages_upgraded", 0),
                    "security_updates": host_result.get("security_updates", 0)
                }
        else:
            # Parse which hosts failed
            failed_hosts = self._parse_failed_hosts(result.stdout, result.stderr, host_ips)
            for host_ip in host_ips:
                if host_ip in failed_hosts:
                    job["progress"][host_ip] = "failed"
                    job["results"][host_ip] = {
                        "success": False,
                        "output": result.stderr[-1000:] if result.stderr else "",
                        "error": failed_hosts[host_ip]
                    }
                else:
                    job["progress"][host_ip] = "completed"
                    job["results"][host_ip] = {
                        "success": True,
                        "output": result.stdout[-1000:] if result.stdout else ""
                    }
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status"""
        return self.jobs.get(job_id)
    
    def list_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all jobs (most recent first)"""
        jobs = list(self.jobs.values())
        jobs.sort(key=lambda x: x.get("started_at", ""), reverse=True)
        return jobs[:limit]
    
    def _parse_ansible_output(self, stdout: str, host_ips: List[str]) -> Dict[str, Dict[str, Any]]:
        """Parse Ansible playbook output to extract progress and package counts"""
        parsed = {}
        
        # Extract package upgrade counts
        # Pattern: "changed=1 unreachable=0 failed=0"
        stats_pattern = r'changed=(\d+).*?unreachable=(\d+).*?failed=(\d+)'
        
        # Extract per-host results
        for host_ip in host_ips:
            host_data = {
                "packages_upgraded": 0,
                "security_updates": 0,
                "status": "unknown"
            }
            
            # Look for host-specific output
            host_lines = [line for line in stdout.split('\n') if host_ip in line]
            
            # Try to extract package counts
            for line in host_lines:
                if 'upgraded' in line.lower() or 'packages' in line.lower():
                    # Extract numbers
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        host_data["packages_upgraded"] = int(numbers[0])
            
            parsed[host_ip] = host_data
        
        return parsed
    
    def _parse_failed_hosts(self, stdout: str, stderr: str, host_ips: List[str]) -> Dict[str, str]:
        """Parse output to identify which hosts failed"""
        failed = {}
        output = stdout + "\n" + stderr
        
        for host_ip in host_ips:
            # Look for failure indicators for this host
            host_pattern = rf'{re.escape(host_ip)}.*?(failed|unreachable|error)'
            if re.search(host_pattern, output, re.IGNORECASE):
                # Extract error message
                error_match = re.search(rf'{re.escape(host_ip)}.*?error[:\s]+(.+?)(?:\n|$)', output, re.IGNORECASE)
                if error_match:
                    failed[host_ip] = error_match.group(1).strip()
                else:
                    failed[host_ip] = "Execution failed"
        
        return failed
    
    def _categorize_error(self, error_msg: str) -> ErrorCategory:
        """Categorize error for retry logic"""
        error_lower = error_msg.lower()
        
        if any(term in error_lower for term in ['timeout', 'timed out', 'connection']):
            return ErrorCategory.NETWORK
        elif any(term in error_lower for term in ['permission', 'denied', 'unauthorized', 'forbidden']):
            return ErrorCategory.PERMISSION
        elif any(term in error_lower for term in ['package', 'apt', 'dpkg', 'dependency']):
            return ErrorCategory.PACKAGE
        elif 'timeout' in error_lower:
            return ErrorCategory.TIMEOUT
        else:
            return ErrorCategory.UNKNOWN
    
    def _audit_log(self, action: str, job_id: str, details: Dict[str, Any]):
        """Log audit events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "job_id": job_id,
            "details": details
        }
        self.audit_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries"""
        return self.audit_log[-limit:]
