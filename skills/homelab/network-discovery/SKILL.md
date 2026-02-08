---
name: network-discovery
version: 1.0.0
description: When the user wants to scan the homelab network, discover network topology, update network-map.md, or perform network inventory. Also use when the user mentions "scan network," "network discovery," "update network map," "network inventory," "discover hosts," or "network topology." This skill automatically scans the environment and updates context/network-map.md.
---

# Network Discovery

You are an expert in network discovery and topology mapping. You scan the homelab environment and automatically update `context/network-map.md` with current network state.

## Guard Rails

**Auto-approve**: Network scanning, topology discovery, reading network configs, updating network-map.md
**Confirm first**: Modifying network configurations, changing IP addresses, deleting network entries

---

## Prerequisites

**Read `context/infrastructure-context.md` first** to know which hosts to scan.

**Required access**:
- SSH access to all hosts (via aliases)
- Pi-hole API access (for DNS records)
- Proxmox API access (for VM/CT IPs)
- Read access to reverse proxy configs

---

## Network Discovery Process

### Step 1: Discover Host IPs and Interfaces

```bash
# Scan all hosts from infrastructure-context.md
HOSTS=(
  "n100uck:10.16.1.18"
  "pve-scratchy:10.16.1.22"
  "pve-itchy:10.16.1.8"
  "opnsense:10.16.1.1"
  "truenas-scale:10.16.1.6"
  "truenas-dr:10.16.1.20"
  "gm-ai:10.16.1.9"
)

# Discover all IPs on each host
for host_info in "${HOSTS[@]}"; do
  IFS=':' read -r alias ip <<< "$host_info"
  echo "=== Scanning $alias ($ip) ==="
  
  # Get all IP addresses
  ssh "$alias" "ip -4 addr show | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.'"
  
  # Get hostname
  ssh "$alias" "hostname"
  
  # Get interfaces and VLANs
  ssh "$alias" "ip addr show | grep -E '^[0-9]+:|inet '"
done
```

### Step 2: Discover Proxmox VMs/CTs

```bash
# Get all VMs/CTs from pve-scratchy
ssh pve-scratchy << 'EOF'
# Get all containers
pct list | awk 'NR>1 {print $1, $2, $3}'

# Get all VMs
qm list | awk 'NR>1 {print $1, $2, $3}'

# For each running CT/VM, get IP
for vmid in $(pct list | awk 'NR>1 && $3=="running" {print $1}'); do
  echo "CT $vmid:"
  pct exec $vmid -- ip -4 addr show | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' || echo "  No IP"
done

for vmid in $(qm list | awk 'NR>1 && $3=="running" {print $1}'); do
  echo "VM $vmid:"
  qm guest exec $vmid -- ip -4 addr show | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' || echo "  No IP"
done
EOF

# Same for pve-itchy
ssh pve-itchy << 'EOF'
pct list | awk 'NR>1 {print $1, $2, $3}'
qm list | awk 'NR>1 {print $1, $2, $3}'
EOF
```

### Step 3: Discover DNS Records (Pi-hole)

```bash
# Query Pi-hole API for custom DNS records
PIHOLE_IP="10.16.1.15"  # VIP
PIHOLE_API_TOKEN=""  # Get from Pi-hole admin

# Get custom DNS records
curl -s "http://${PIHOLE_IP}/admin/api.php?customdns&auth=${PIHOLE_API_TOKEN}" | \
  jq -r '.data[] | "\(.domain) -> \(.ip)"'

# Get all local DNS records (including *.gmdojo.tech)
curl -s "http://${PIHOLE_IP}/admin/api.php?getAllCustomRecords&auth=${PIHOLE_API_TOKEN}" | \
  jq -r '.[] | "\(.domain) -> \(.ip)"'
```

**Alternative**: SSH to Pi-hole and read config directly:
```bash
ssh piholed "cat /etc/pihole/custom.list | grep -v '^#'"
```

### Step 4: Discover Reverse Proxy Routes

#### Nginx Proxy Manager (CT 200)

```bash
# Access NPM database or config
ssh nginx-proxy-manager << 'EOF'
# NPM stores configs in SQLite or JSON
# Check for config files
find /data -name "*.json" -o -name "*.db" 2>/dev/null | head -5

# Or check nginx configs
find /data/nginx -name "*.conf" 2>/dev/null | head -5
EOF
```

#### Traefik (CT 123)

```bash
ssh traefik << 'EOF'
# Traefik dynamic config
cat /etc/traefik/traefik.yml 2>/dev/null || echo "Config not found"
cat /etc/traefik/dynamic/*.yml 2>/dev/null || echo "Dynamic configs not found"

# Or check Docker labels if Traefik is containerized
docker ps --format "{{.Names}}: {{.Label \"traefik.http.routers\"}}"
EOF
```

### Step 5: Discover VLANs and Subnets

```bash
# Check Proxmox bridges and VLANs
ssh pve-scratchy "cat /etc/network/interfaces | grep -E 'bridge|vlan'"

# Check OPNsense VLANs
ssh opnsense "ifconfig | grep -E 'vlan|bridge'"

# Scan for active subnets
for subnet in 10.16.1.0/24 10.16.66.0/24 10.16.10.0/24; do
  echo "=== Scanning $subnet ==="
  nmap -sn $subnet 2>/dev/null | grep -E "Nmap scan|for " || echo "nmap not available"
done
```

### Step 6: Discover VIPs (keepalived)

```bash
# Check keepalived status on primary
ssh piholed << 'EOF'
# Check keepalived config
cat /etc/keepalived/keepalived.conf | grep -E "virtual_ipaddress|virtual_router_id"

# Check current VIP status
ip addr show | grep "10.16.1.15" && echo "VIP active on this host"
EOF

# Check on secondary
ssh n100uck << 'EOF'
ip addr show | grep "10.16.1.15" && echo "VIP active on this host" || echo "VIP not active"
EOF
```

### Step 7: Discover Tailscale Nodes

```bash
# Check Tailscale status
ssh tailscaler "tailscale status"
ssh cp-tailscale "tailscale status"

# Get Tailscale IPs
ssh tailscaler "tailscale ip -4"
ssh cp-tailscale "tailscale ip -4"
```

---

## Generate Updated network-map.md

### Create Discovery Script

```bash
cat > /tmp/network-discovery.sh << 'SCRIPT'
#!/bin/bash
# Network Discovery Script
# Scans homelab and generates network-map.md

OUTPUT_FILE="context/network-map.md"
DATE=$(date +%Y-%m-%d)

cat > "$OUTPUT_FILE" << EOF
# Network Map

Network topology and addressing for the Get Massive Dojo homelab.

**Last Updated**: ${DATE}
**Generated by**: network-discovery skill

## Subnet Layout

### Primary LAN: 10.16.1.0/24 (VLAN 1)

| IP | Hostname | Role | Source |
|----|----------|------|--------|
EOF

# Discover and add entries
# (Insert discovered IPs here)

cat >> "$OUTPUT_FILE" << EOF

### IoT VLAN: 10.16.66.0/24 (VLAN 66)

| IP | Hostname | Role | Source |
|----|----------|------|--------|
EOF

# Discover VLAN 66 entries

cat >> "$OUTPUT_FILE" << EOF

### Tailscale: 10.16.10.0/24 (VLAN 10)

| IP | Hostname | Role | Source |
|----|----------|------|--------|
EOF

# Discover Tailscale entries

cat >> "$OUTPUT_FILE" << EOF

## Virtual IPs (VIPs)

| VIP | Purpose | Protocol | Primary | Secondary |
|-----|---------|----------|---------|-----------|
EOF

# Discover VIPs

cat >> "$OUTPUT_FILE" << EOF

## DNS Configuration

### Internal DNS (Pi-hole)

**Service IP**: 10.16.1.15 (VIP, auto-failover)
- Primary: piholed (10.16.1.16)
- Secondary: n100uck (10.16.1.18)

### Local DNS Records (*.gmdojo.tech -> 10.16.1.50)

| Domain | Points To | Service |
|--------|-----------|---------|
EOF

# Discover DNS records

cat >> "$OUTPUT_FILE" << EOF

## Reverse Proxy Architecture

### Primary: Nginx Proxy Manager (CT 200, 10.16.1.50)
- Admin: port 81
- HTTP: port 8080
- HTTPS: port 8443

### Auth Layer: Traefik + Authelia (CT 123 + CT 122)
- Traefik: HTTP/80, HTTPS/443, Dashboard/8080 (10.16.1.26)
- Authelia: SSO on port 9091 (10.16.1.25, auth.gmdojo.tech)

## Tailscale

- **Subnet routing**: Via TrueNAS for homelab access
- **Nodes**: [discovered nodes]

## Notification Channels

| Channel | Endpoint | Purpose |
|---------|----------|---------|
| ntfy (consolidated) | https://ntfy.sh/homelab-status | All monitoring alerts |
EOF

echo "Network map generated: $OUTPUT_FILE"
SCRIPT

chmod +x /tmp/network-discovery.sh
```

---

## Complete Discovery Workflow

### Run Full Network Discovery

```bash
# Create discovery script that collects all data
cat > /tmp/full-network-discovery.sh << 'EOF'
#!/bin/bash
set -e

OUTPUT="context/network-map.md"
TEMP_DIR="/tmp/network-discovery-$$"
mkdir -p "$TEMP_DIR"

echo "Starting network discovery..."

# 1. Discover physical hosts
echo "Discovering physical hosts..."
for alias in n100uck pve-scratchy pve-itchy opnsense truenas-scale truenas-dr gm-ai; do
  if ssh -o ConnectTimeout=5 "$alias" "hostname" &>/dev/null; then
    hostname=$(ssh "$alias" "hostname")
    ip=$(ssh "$alias" "hostname -I | awk '{print \$1}'")
    echo "| $ip | $hostname | [role] | Physical |" >> "$TEMP_DIR/hosts.txt"
  fi
done

# 2. Discover Proxmox VMs/CTs
echo "Discovering Proxmox VMs/CTs..."
ssh pve-scratchy << 'PVE_SCRIPT' > "$TEMP_DIR/pve-scratchy.txt"
for vmid in $(pct list | awk 'NR>1 && $3=="running" {print $1}'); do
  name=$(pct config $vmid | grep "hostname:" | awk '{print $2}')
  ip=$(pct exec $vmid -- ip -4 addr show 2>/dev/null | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' | head -1)
  if [ -n "$ip" ]; then
    echo "| $ip | $name | CT $vmid | Proxmox |"
  fi
done
for vmid in $(qm list | awk 'NR>1 && $3=="running" {print $1}'); do
  name=$(qm config $vmid | grep "name:" | awk '{print $2}')
  ip=$(qm guest exec $vmid -- ip -4 addr show 2>/dev/null | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' | head -1)
  if [ -n "$ip" ]; then
    echo "| $ip | $name | VM $vmid | Proxmox |"
  fi
done
PVE_SCRIPT

# 3. Discover DNS records
echo "Discovering DNS records..."
ssh piholed "cat /etc/pihole/custom.list 2>/dev/null | grep -v '^#' | grep -v '^$'" > "$TEMP_DIR/dns.txt" || true

# 4. Discover VIPs
echo "Discovering VIPs..."
if ssh piholed "ip addr show | grep -q '10.16.1.15'"; then
  echo "VIP 10.16.1.15 active on piholed" >> "$TEMP_DIR/vips.txt"
fi

# 5. Generate network-map.md
echo "Generating network-map.md..."
# (Insert markdown generation logic here)

echo "Discovery complete. Review $OUTPUT"
EOF

chmod +x /tmp/full-network-discovery.sh
```

---

## Verify After

1. **network-map.md updated**: Check timestamp and content
2. **All hosts discovered**: Compare against infrastructure-context.md
3. **DNS records found**: Verify Pi-hole records are captured
4. **VIPs documented**: Check keepalived VIPs are listed
5. **Subnets complete**: Verify all VLANs are documented

---

## Rollback

Network discovery is read-only (except for updating network-map.md). To rollback:

```bash
git checkout HEAD -- context/network-map.md
```

---

## Troubleshooting

### Host unreachable
- Check SSH connectivity: `ssh <alias> "hostname"`
- Verify host is in infrastructure-context.md
- Check if host is powered on

### Pi-hole API access denied
- Use SSH method instead: `ssh piholed "cat /etc/pihole/custom.list"`
- Or get API token from Pi-hole admin UI

### Proxmox API unavailable
- Use SSH with `pct` and `qm` commands instead
- Verify Proxmox host is accessible

### Missing DNS records
- Check Pi-hole custom.list file
- Verify DNS sync is working (if using HA)

---

## Related Skills

- **linux-networking** - Network configuration and troubleshooting
- **dns-management** - Pi-hole DNS management
- **proxmox-networking** - Proxmox network configuration
- **homelab-services** - Service discovery and inventory
