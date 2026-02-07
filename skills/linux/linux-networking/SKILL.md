---
name: linux-networking
version: 1.0.0
description: When the user wants to configure or troubleshoot Linux networking -- IP addresses, routing, DNS resolution, interfaces, Tailscale, or connectivity issues. Also use when the user mentions "network config," "IP address," "routing table," "DNS not resolving," "can't ping," or "Tailscale." For Proxmox-specific networking (bridges, VLANs), see proxmox-networking. For DNS management (Pi-hole), see dns-management.
---

# Linux Networking

You are an expert in Linux networking. Operations target the Get Massive Dojo homelab on the 10.16.1.0/24 subnet.

## Initial Assessment

**Read `context/network-map.md` first** for the full network topology, VIPs, and DNS configuration.

Before making changes:
1. **Identify the host** and its current network configuration
2. **Check impact** - Will changes affect other hosts or services?
3. **Document current state** before modifying anything

## Guard Rails

**Auto-approve**: Connectivity tests, DNS queries, route viewing, interface status
**Confirm first**: IP address changes, route modifications, interface down operations

---

## Connectivity Diagnostics

### Quick Connectivity Check
```bash
# From local machine to all infrastructure
for host in 10.16.1.22 10.16.1.8 10.16.1.6 10.16.1.20 10.16.1.18 10.16.1.9 10.16.1.1; do
  ping -c 1 -W 2 $host > /dev/null 2>&1 && echo "Y $host" || echo "X $host"
done
```

### Full Host Connectivity Sweep
```bash
for host in n100uck pve-scratchy pve-itchy opnsense truenas-scale truenas-dr piholed gm-ai dockc nginx-proxy-manager; do
    echo -n "$host: "
    ssh -o ConnectTimeout=5 -o BatchMode=yes $host "hostname && uptime" 2>&1 | tr '\n' ' '
    echo ""
done
```

### Check Open Ports
```bash
ssh <alias> "ss -tlnp"
```

### Check Active Connections
```bash
ssh <alias> "ss -tunp"
```

### Traceroute
```bash
ssh <alias> "traceroute <destination>"
```

---

## Interface Configuration

### View Interfaces
```bash
ssh <alias> "ip addr show"
ssh <alias> "ip link show"
```

### View Routing Table
```bash
ssh <alias> "ip route show"
```

### Check Default Gateway
```bash
ssh <alias> "ip route | grep default"
```

### View ARP Table
```bash
ssh <alias> "ip neigh show"
```

---

## DNS Troubleshooting

### Test DNS via VIP (Pi-hole HA)
```bash
dig @10.16.1.15 google.com +short
```

### Test DNS via Primary Pi-hole
```bash
dig @10.16.1.16 google.com +short
```

### Test DNS via Secondary Pi-hole
```bash
dig @10.16.1.18 google.com +short
```

### Test Internal DNS Records
```bash
dig @10.16.1.15 pve.gmdojo.tech +short
# Expected: 10.16.1.50
```

### Check resolv.conf
```bash
ssh <alias> "cat /etc/resolv.conf"
# Should point to 10.16.1.15 (Pi-hole VIP)
```

### Fix DNS Resolution
```bash
ssh <alias> << 'EOF'
echo "nameserver 10.16.1.15" > /etc/resolv.conf
echo "nameserver 1.1.1.1" >> /etc/resolv.conf
EOF
```

---

## Tailscale

### Check Tailscale Status
```bash
ssh <alias> "tailscale status"
```

### Check Tailscale IP
```bash
ssh <alias> "tailscale ip -4"
```

### Tailscale Nodes in Lab
- tailscaler (CT 901, 10.16.1.31)
- cp-tailscale (CT 117, 10.16.10.2)
- dp-macbook-secondary (100.86.205.100)

### Restart Tailscale
```bash
ssh <alias> "systemctl restart tailscaled"
```

---

## Network Scanning

### WatchYourLAN (Network Scanner)
```bash
# Query WatchYourLAN API
curl -s http://10.16.1.17:8840/api/all | python3 -m json.tool
```

### Quick Port Scan (from any host)
```bash
ssh <alias> "nmap -sT -p 22,80,443,8006,8080,8081 <target_ip>"
```

---

## Static IP Configuration (Debian)

### View Current Config
```bash
ssh <alias> "cat /etc/network/interfaces"
```

### Set Static IP
```bash
ssh <alias> << 'EOF'
cat > /etc/network/interfaces.d/<iface> << 'NETEOF'
auto <iface>
iface <iface> inet static
    address <ip>/24
    gateway 10.16.1.1
    dns-nameservers 10.16.1.15
NETEOF
systemctl restart networking
EOF
```

### Verify After
```bash
ssh <alias> "ip addr show <iface>"
ssh <alias> "ip route | grep default"
ssh <alias> "ping -c 1 10.16.1.1"
```

---

## Troubleshooting

### Host Unreachable
1. **Check ping**: `ping -c 3 <ip>`
2. **Check SSH port**: `nc -zv <ip> 22`
3. **Check from Proxmox**: `ssh pve-scratchy "pct exec <CTID> -- ip addr"`
4. **Check gateway**: `ssh <alias> "ping -c 1 10.16.1.1"`

### DNS Not Resolving
1. **Test VIP**: `dig @10.16.1.15 google.com`
2. **Test primary**: `dig @10.16.1.16 google.com`
3. **Test secondary**: `dig @10.16.1.18 google.com`
4. **Check Pi-hole**: `ssh piholed "systemctl status pihole-FTL"`
5. **Check resolv.conf**: `ssh <alias> "cat /etc/resolv.conf"`

### Network Slow
```bash
ssh <alias> << 'EOF'
echo "=== Network Diagnostics ==="
echo "--- Interface Stats ---"
ip -s link show
echo ""
echo "--- Connection Count ---"
ss -s
echo ""
echo "--- Top Bandwidth Consumers ---"
ss -tnp | awk '{print $5}' | sort | uniq -c | sort -rn | head -10
EOF
```

---

## Related Skills

- **proxmox-networking** - Proxmox bridges, VLANs, SDN
- **dns-management** - Pi-hole administration
- **reverse-proxy** - Traefik and NPM routing
