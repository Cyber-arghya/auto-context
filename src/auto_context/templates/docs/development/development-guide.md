# Development: Workflow & Operational Guide

## Getting Started
1. Install project dependencies following repository package manifests.
2. Configure local environment variables in `.env` based on `.env.example`.
3. Run verification test suite to ensure the environment is healthy.

## Architecture Invariants & Traps (Gotchas)
> ⚡ **Institutional Knowledge:** Record non-obvious failure modes, port collisions, toolchain quirks, and environment traps discovered in {{PROJECT_NAME}}. Do NOT record transient bugs or resolved error logs.

1. **Deterministic State:** Verify that build and test commands run cleanly with exit code 0.
2. **Secret Safety:** Never commit active tokens, private keys, or credentials into git.
