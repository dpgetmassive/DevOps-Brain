---
name: dns-management
version: 1.0.0
description: When the user wants to manage DNS -- Pi-hole administration, custom DNS records, gravity sync, block lists, keepalived failover, or DNS troubleshooting. Also use when the user mentions "Pi-hole," "DNS record," "block list," "gravity," "DNS not working," "VIP," or "keepalived." For general networking, see linux-networking.
---

# DNS Management (Pi-hole HA)

You are an expert in Pi-hole DNS management with HA failover.

## DNS Architecture

**Read `context/network-map.md` first** for the full DNS configuration.

| Component | Host | IP | Role |
|-----------|------|-----|------|
| Pi-hole Primary | piholed (CT 111) | 10.16.1.16 | Master DNS, priority 100 |
| Pi-hole Secondary | n100uck | 10.16.1.18 | Backup DNS, priority 90 |
| DNS VIP | keepalived | 10.16.1.15 | Floating IP, auto-failover |
| Pi-hole version | -- | -- | v6.2.2 |
| Upstream DNS | Cloudflare | 1.1.1.1, 1.0.0.1 | External resolution |

**Web UIs**: http://10.16.1.15/admin (VIP), http://10.16.1.16/admin, http://10.16.1.18/admin

## Guard Rails

**Auto-approve**: DNS queries, status checks, gravity updates, viewing records
**Confirm first**: Keepalived config changes, upstream DNS changes, disabling Pi-hole

---

## Quick Status Check

### DNS Resolution Test
```bash
dig @10.16.1.15 google.com +short         # Via VIP
dig @10.16.1.16 google.com +short         # Via primary
dig @10.16.1.18 google.com +short         # Via secondary
dig @10.16.1.15 pve.gmdojo.tech +short    # Internal record
```

### Check VIP Location
```bash
ssh piholed "ip a show eth0 | grep 10.16.1.15"
ssh n100uck "ip a show enp3s0 | grep 10.16.1.15"
```

### Pi-hole Service Status
```bash
ssh piholed "systemctl status pihole-FTL --no-pager"
ssh n100uck "systemctl status pihole-FTL --no-pager"
```

### Keepalived Status
```bash
ssh piholed "systemctl status keepalived --no-pager"
ssh n100uck "systemctl status keepalived --no-pager"
```

---

## Custom DNS Records

### Current Local DNS Records
All `*.gmdojo.tech` domains resolve to 10.16.1.50 (NPM) for reverse proxy routing.

### Add/Modify DNS Record
**Edit on primary only** -- changes sync hourly to secondary:

```bash
ssh piholed << 'EOF'
# Edit pihole.toml [dns] -> hosts = []
nano /etc/pihole/pihole.toml
systemctl restart pihole-FTL
EOF
```

### Manual DNS Sync (Don't Wait for Hourly Cron)
```bash
ssh piholed "/root/sync-pihole-dns.sh"
```

### Check Sync Status
```bash
ssh piholed "tail -20 /var/log/pihole-dns-sync.log"
```

### Verify Record on Both Nodes
```bash
dig @10.16.1.16 <domain> +short
dig @10.16.1.18 <domain> +short
```

---

## Block List Management

### Update Gravity (Block Lists)
```bash
ssh piholed "pihole -g"
```

### View Block List Stats
```bash
ssh piholed "pihole -c"
```

### Check Query Log
```bash
ssh piholed "pihole -t"  # Tail log
```

---

## Keepalived Failover

### Test Failover
```bash
# 1. Check VIP is on primary
ssh piholed "ip a show eth0 | grep 10.16.1.15"

# 2. Stop keepalived on primary (triggers failover)
ssh piholed "systemctl stop keepalived"

# 3. Wait and verify VIP moved
sleep 5
ssh n100uck "ip a show enp3s0 | grep 10.16.1.15"

# 4. Test DNS still works
dig @10.16.1.15 google.com +short

# 5. Restore primary
ssh piholed "systemctl start keepalived"

# 6. Verify VIP returned
sleep 5
ssh piholed "ip a show eth0 | grep 10.16.1.15"
```

### Keepalived Config
- Primary config: `/etc/keepalived/keepalived.conf` on piholed
- Secondary config: `/etc/keepalived/keepalived.conf` on n100uck
- Virtual Router ID: 15
- Auth: PASS (piholedns2025)

---

## Gravity Sync (Config Replication)

### Compare Configs
```bash
ssh piholed "gravity-sync compare"
```

### Push Primary to Secondary
```bash
ssh piholed "gravity-sync push"
```

### Alternative: Use Teleporter
1. Access http://10.16.1.16/admin
2. Settings -> Teleporter -> Generate backup
3. Apply to secondary via http://10.16.1.18/admin

---

## Troubleshooting

### DNS Not Resolving
```bash
# 1. Test VIP
dig @10.16.1.15 google.com

# 2. Test each node
dig @10.16.1.16 google.com
dig @10.16.1.18 google.com

# 3. Check Pi-hole service
ssh piholed "systemctl status pihole-FTL --no-pager"
ssh n100uck "systemctl status pihole-FTL --no-pager"

# 4. Check VIP
ssh piholed "ip a | grep 10.16.1.15"
ssh n100uck "ip a | grep 10.16.1.15"

# 5. Check resolv.conf on affected host
ssh <alias> "cat /etc/resolv.conf"
```

### VIP Not Moving (Split Brain)
```bash
# Check for VRRP issues
ssh piholed "journalctl -u keepalived -S '5 min ago' --no-pager"
ssh n100uck "journalctl -u keepalived -S '5 min ago' --no-pager"

# Restart secondary keepalived
ssh n100uck "systemctl restart keepalived"
```

### DNS Sync Failing
```bash
# Check sync log
ssh piholed "tail -20 /var/log/pihole-dns-sync.log"

# Check SSH to secondary
ssh piholed "ssh -o ConnectTimeout=5 root@10.16.1.18 echo ok"

# Manual sync
ssh piholed "/root/sync-pihole-dns.sh"
```

---

## Related Skills

- **linux-networking** - General network troubleshooting
- **reverse-proxy** - Services that DNS records point to
- **monitoring-ops** - DNS monitoring alerts
