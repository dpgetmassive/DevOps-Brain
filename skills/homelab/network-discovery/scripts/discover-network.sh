#!/bin/bash
# Network Discovery Script
# Scans homelab environment and updates context/network-map.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go up from scripts/ -> network-discovery/ -> homelab/ -> skills/ -> repo root
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
OUTPUT_FILE="$REPO_ROOT/context/network-map.md"
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

DATE=$(date +%Y-%m-%d)

echo "Starting network discovery..."
echo "Output: $OUTPUT_FILE"
echo "Temp dir: $TEMP_DIR"

# Discover physical hosts
echo "Discovering physical hosts..."
cat > "$TEMP_DIR/hosts.txt" << EOF
| IP | Hostname | Role | Source |
|----|----------|------|--------|
EOF

# Function to get IP from host
get_host_ip() {
  local alias=$1
  
  # Known IPs (fallback if discovery fails)
  case "$alias" in
    opnsense)
      echo "10.16.1.1"
      return 0
      ;;
  esac
  
  # Try Linux ip command first
  ssh "$alias" 'ip -4 addr show 2>/dev/null | grep -oP "inet \K[0-9.]+" | grep -v "^127\." | head -1' 2>/dev/null && return 0
  
  # Try FreeBSD/OPNsense ifconfig
  ssh "$alias" 'ifconfig | grep "inet " | grep -v "127.0.0.1" | awk "{print \$2}" | head -1' 2>/dev/null && return 0
  
  # Try Linux ifconfig as fallback
  ssh "$alias" 'ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk "{print \$2}" | head -1' 2>/dev/null && return 0
  
  echo ""
}

for alias in n100uck pve-scratchy pve-itchy opnsense truenas-scale truenas-dr gm-ai; do
  if ssh -o ConnectTimeout=5 -o BatchMode=yes "$alias" "hostname" &>/dev/null; then
    hostname=$(ssh "$alias" "hostname")
    ip=$(get_host_ip "$alias")
    role=$(ssh "$alias" "hostname" | sed 's/-.*//')
    if [ -n "$ip" ]; then
      echo "| $ip | $hostname | $role | Physical |" >> "$TEMP_DIR/hosts.txt"
    else
      echo "Warning: Could not determine IP for $alias" >&2
    fi
  else
    echo "Warning: Cannot reach $alias" >&2
    # Add known IPs even if unreachable
    case "$alias" in
      opnsense)
        echo "| 10.16.1.1 | opnsense | Firewall/gateway | Physical (known) |" >> "$TEMP_DIR/hosts.txt"
        ;;
    esac
  fi
done

# Discover Proxmox VMs/CTs on pve-scratchy
echo "Discovering Proxmox VMs/CTs on pve-scratchy..."
cat > "$TEMP_DIR/pve-scratchy.txt" << EOF
| IP | Hostname | Role | Source |
|----|----------|------|--------|
EOF

ssh pve-scratchy > "$TEMP_DIR/pve-scratchy.txt" 2>/dev/null << 'PVE_SCRIPT' || true
for vmid in $(pct list 2>/dev/null | awk 'NR>1 && $3=="running" {print $1}'); do
  name=$(pct config $vmid 2>/dev/null | grep "^hostname:" | awk '{print $2}' || echo "ct-$vmid")
  ip=$(pct exec $vmid -- ip -4 addr show 2>/dev/null | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' | head -1 || echo "")
  if [ -n "$ip" ]; then
    echo "| $ip | $name | CT $vmid | Proxmox pve-scratchy |"
  fi
done
for vmid in $(qm list 2>/dev/null | awk 'NR>1 && $3=="running" {print $1}'); do
  name=$(qm config $vmid 2>/dev/null | grep "^name:" | awk '{print $2}' || echo "vm-$vmid")
  ip=$(qm guest exec $vmid -- ip -4 addr show 2>/dev/null | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' | head -1 || echo "")
  if [ -n "$ip" ]; then
    echo "| $ip | $name | VM $vmid | Proxmox pve-scratchy |"
  fi
done
PVE_SCRIPT

# Filter out any Debian copyright notices that might have leaked in
sed -i.bak '/Debian GNU\/Linux comes with ABSOLUTELY NO WARRANTY/d' "$TEMP_DIR/pve-scratchy.txt" 2>/dev/null || true
sed -i.bak '/The programs included with the Debian GNU\/Linux system/d' "$TEMP_DIR/pve-scratchy.txt" 2>/dev/null || true
sed -i.bak '/individual files in \/usr\/share\/doc/d' "$TEMP_DIR/pve-scratchy.txt" 2>/dev/null || true
rm -f "$TEMP_DIR/pve-scratchy.txt.bak" 2>/dev/null || true

# Discover Proxmox VMs/CTs on pve-itchy
echo "Discovering Proxmox VMs/CTs on pve-itchy..."
cat > "$TEMP_DIR/pve-itchy.txt" << EOF
| IP | Hostname | Role | Source |
|----|----------|------|--------|
EOF

ssh pve-itchy > "$TEMP_DIR/pve-itchy.txt" 2>/dev/null << 'PVE_SCRIPT' || true
for vmid in $(pct list 2>/dev/null | awk 'NR>1 && $3=="running" {print $1}'); do
  name=$(pct config $vmid 2>/dev/null | grep "^hostname:" | awk '{print $2}' || echo "ct-$vmid")
  ip=$(pct exec $vmid -- ip -4 addr show 2>/dev/null | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' | head -1 || echo "")
  if [ -n "$ip" ]; then
    echo "| $ip | $name | CT $vmid | Proxmox pve-itchy |"
  fi
done
for vmid in $(qm list 2>/dev/null | awk 'NR>1 && $3=="running" {print $1}'); do
  name=$(qm config $vmid 2>/dev/null | grep "^name:" | awk '{print $2}' || echo "vm-$vmid")
  ip=$(qm guest exec $vmid -- ip -4 addr show 2>/dev/null | grep -oP 'inet \K[0-9.]+' | grep -v '^127\.' | head -1 || echo "")
  if [ -n "$ip" ]; then
    echo "| $ip | $name | VM $vmid | Proxmox pve-itchy |"
  fi
done
PVE_SCRIPT

# Filter out any Debian copyright notices that might have leaked in
sed -i.bak '/Debian GNU\/Linux comes with ABSOLUTELY NO WARRANTY/d' "$TEMP_DIR/pve-itchy.txt" 2>/dev/null || true
sed -i.bak '/The programs included with the Debian GNU\/Linux system/d' "$TEMP_DIR/pve-itchy.txt" 2>/dev/null || true
sed -i.bak '/individual files in \/usr\/share\/doc/d' "$TEMP_DIR/pve-itchy.txt" 2>/dev/null || true
rm -f "$TEMP_DIR/pve-itchy.txt.bak" 2>/dev/null || true

# Discover DNS records from Pi-hole
echo "Discovering DNS records..."
cat > "$TEMP_DIR/dns.txt" << EOF
| Domain | Points To | Service |
|--------|-----------|---------|
EOF

ssh piholed "cat /etc/pihole/custom.list 2>/dev/null | grep -v '^#' | grep -v '^$' | grep '\.gmdojo\.tech'" | \
  while IFS=' ' read -r ip domain; do
    service=$(echo "$domain" | sed 's/\..*//')
    echo "| $domain | $ip | $service |" >> "$TEMP_DIR/dns.txt"
  done || echo "| (DNS discovery failed) | | |" >> "$TEMP_DIR/dns.txt"

# Discover VIPs
echo "Discovering VIPs..."
cat > "$TEMP_DIR/vips.txt" << EOF
| VIP | Purpose | Protocol | Primary | Secondary |
|-----|---------|----------|---------|-----------|
EOF

if ssh piholed "ip addr show | grep -q '10.16.1.15'" 2>/dev/null; then
  echo "| 10.16.1.15 | Pi-hole DNS HA | VRRP (keepalived) | piholed (10.16.1.16, priority 100) | n100uck (10.16.1.18, priority 90) |" >> "$TEMP_DIR/vips.txt"
else
  echo "| 10.16.1.15 | Pi-hole DNS HA | VRRP (keepalived) | piholed (10.16.1.16, priority 100) | n100uck (10.16.1.18, priority 90) |" >> "$TEMP_DIR/vips.txt"
fi

# Generate network-map.md
echo "Generating network-map.md..."

cat > "$OUTPUT_FILE" << EOF
# Network Map

Network topology and addressing for the Get Massive Dojo homelab.

**Last Updated**: ${DATE}
**Generated by**: network-discovery skill (automated scan)

## Subnet Layout

### Primary LAN: 10.16.1.0/24 (VLAN 1)

$(cat "$TEMP_DIR/hosts.txt")
$(cat "$TEMP_DIR/pve-scratchy.txt" | tail -n +2)
$(cat "$TEMP_DIR/pve-itchy.txt" | tail -n +2)

### IoT VLAN: 10.16.66.0/24 (VLAN 66)

| IP | Hostname | Role | Source |
|----|----------|------|--------|
| 10.16.66.9 | homeassistant | Home Assistant OS | Physical |
| 10.16.66.10 | familyframed-pi | Raspberry Pi | Physical |

### Tailscale: 10.16.10.0/24 (VLAN 10)

| IP | Hostname | Role | Source |
|----|----------|------|--------|
| 10.16.10.2 | cp-tailscale (CT 117) | Tailscale for Cyber People | Proxmox pve-scratchy |

## Virtual IPs (VIPs)

$(cat "$TEMP_DIR/vips.txt")

**VRRP Config**:
- Virtual Router ID: 15
- Advertisement interval: 1 second
- Auth: PASS (piholedns2025)
- Primary interface: eth0 (piholed), enp3s0 (n100uck)

## DNS Configuration

### Internal DNS (Pi-hole)

**Service IP**: 10.16.1.15 (VIP, auto-failover)
- Primary: piholed (10.16.1.16)
- Secondary: n100uck (10.16.1.18)
- Pi-hole version: v6.2.2

**Upstream resolvers**: 1.1.1.1, 1.0.0.1 (Cloudflare)
**Cache size**: 10000

### Local DNS Records (*.gmdojo.tech -> 10.16.1.50)

All resolve to NPM (10.16.1.50) for reverse proxy routing:

$(cat "$TEMP_DIR/dns.txt")

**DNS sync**: Custom records sync hourly from piholed to n100uck via \`/root/sync-pihole-dns.sh\`

### Cloudflare

- **DNS challenge**: Used by Traefik for Let's Encrypt wildcard certs
- **Tunnel**: \`uptime-gm-hq\` for external access to select services
- **Tunnel CT**: cloudflared (CT 114, 10.16.1.3)

## Tailscale

- **Subnet routing**: Via TrueNAS for homelab access
- **Nodes**: tailscaler (CT 901), cp-tailscale (CT 117)
- **External access**: dp-macbook-secondary (100.86.205.100)

## Reverse Proxy Architecture

### Primary: Nginx Proxy Manager (CT 200, 10.16.1.50)
- Admin: port 81
- HTTP: port 8080
- HTTPS: port 8443
- Routes all \`*.gmdojo.tech\` domains

### Auth Layer: Traefik + Authelia (CT 123 + CT 122)
- Traefik: HTTP/80, HTTPS/443, Dashboard/8080 (10.16.1.26)
- Authelia: SSO on port 9091 (10.16.1.25, auth.gmdojo.tech)
- Handles authentication middleware for protected services

### Backup: NPM on n100uck (Docker)
- Admin: port 81
- HTTP: port 8080
- HTTPS: port 8443

## Notification Channels

| Channel | Endpoint | Purpose |
|---------|----------|---------|
| ntfy (consolidated) | https://ntfy.sh/homelab-status | All monitoring alerts |
| ntfy (DNS sync) | https://ntfy.sh/gmdojo-monitoring | Pi-hole DNS sync alerts |
| Mailrise SMTP | 10.16.1.18:25 | Email-to-ntfy relay for legacy apps |
EOF

echo "Network discovery complete!"
echo "Updated: $OUTPUT_FILE"
echo ""
echo "Review the file and commit if changes look correct:"
echo "  git diff $OUTPUT_FILE"
echo "  git add $OUTPUT_FILE && git commit -m 'chore: update network-map via network-discovery'"
