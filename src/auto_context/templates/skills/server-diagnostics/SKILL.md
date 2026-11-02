---
name: server-diagnostics
version: 1.0.0
description: Real-time system health checks, RAM/swap usage, CPU load, open ports, and network connectivity diagnostics.
triggers: ["health", "ram", "memory-check", "cpu", "ports", "disk", "diagnostics", "server-status"]
---

# Skill: Server Diagnostics & System Health Inspection

## Overview
Standard operational procedures for inspecting host resources, diagnosing memory bottlenecks, verifying open network sockets, and monitoring process execution across Linux, WSL2, and POSIX containers.

## When to Activate
- When experiencing high RAM/swap usage or CPU thrashing during builds or runtime execution.
- When a service fails to bind to a local port (e.g. `EADDRINUSE`).
- When diagnosing slow disk I/O, zombie processes, or container health degradation.

## Diagnostic Procedures & Runbooks

### 1. Memory & Swap Health
```bash
# High-density real-time RAM and swap utilization in MB
free -m -h

# Top 10 memory-consuming processes
ps aux --sort=-%mem | head -n 11 | awk '{print $2, $3, $4, $11}'
```

### 2. CPU Load & Process Throttling
```bash
# Instant load averages (1m, 5m, 15m) and core counts
uptime
nproc

# Top CPU-consuming processes (snapshot)
ps aux --sort=-%cpu | head -n 11 | awk '{print $2, $3, $4, $11}'
```

### 3. Disk Space & Inode Saturation
```bash
# Check filesystem capacity (human-readable)
df -hT -x tmpfs -x devtmpfs

# Check inode usage (prevents silent disk-full errors despite free space)
df -i /
```

### 4. Open Network Ports & Sockets
```bash
# Check all active TCP/UDP listening sockets with process names
sudo ss -tulpn

# Verify internet DNS resolution
nslookup cloudflare.com 1.1.1.1
```

### 5. Project Directory & Service Path Resolution
- **Dynamic Server Path Identification:**
  ```bash
  # Check current server working directory
  pwd
  
  # Locate systemd service working directory
  systemctl show <service_name> --property=WorkingDirectory
  
  # Inspect Docker container working directory
  docker inspect --format '{{.Config.WorkingDir}}' <container_id>
  ```
- **Privacy Invariant:** Machine-specific filesystem paths (e.g. `C:\Users\...` or `/home/...`) belong strictly to local runtime environments and must never be committed to public git history or public docs.
