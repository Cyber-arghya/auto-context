---
name: server-diagnostics
version: 1.0.0
description: Real-time system health checks, RAM/swap usage, CPU load, open ports, and network connectivity diagnostics.
triggers: ["health", "ram", "cpu", "swap", "diagnostics", "server", "port", "disk", "uptime"]
---

# Skill: Server Diagnostics & Resource Health

## Overview
Comprehensive runbook for assessing server stability, inspecting hardware memory buffers, verifying swap allocation, auditing listening network ports, and monitoring active background processes.

## When to Activate
- When experiencing system slowdowns, high latency, or OOM (Out-Of-Memory) kill events.
- When checking server resource headroom before running heavy builds or containers.
- When verifying open ports, firewall status, or Cloudflare tunnel connectivity.

## Workflows & Procedures

### 1. Memory & Buffer Diagnostics
```bash
# Check physical RAM and swap file availability
free -h

# Check top 5 memory-consuming processes
ps aux --sort=-%mem | head -n 6
```
* **Critical Threshold:** Available memory below 200MB warrants immediate cache cleanup or swap expansion.

### 2. CPU Load & Process Monitoring
```bash
# Check system uptime and 1m, 5m, 15m load averages
uptime

# Check top 5 CPU-consuming processes
ps aux --sort=-%cpu | head -n 6
```

### 3. Disk Storage & Inode Health
```bash
# Inspect filesystem disk usage
df -h /

# Inspect inode utilization (detects micro-file exhaustion)
df -i /
```

### 4. Network Ports & Connectivity Audit
```bash
# Check all active TCP/UDP listening sockets with process names
sudo ss -tulpn

# Verify internet DNS resolution
nslookup cloudflare.com 1.1.1.1
```
