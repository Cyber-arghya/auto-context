# Critical Gotchas, Anti-Patterns & Architecture Invariants

> Institutional knowledge and non-obvious traps that cannot be guessed from reading code.

## ⚠️ Active Constraints & Traps

1. **Port Invariants:** Inspect discovered ports before binding local services.
2. **Secret Isolation:** Production secrets belong in `.env`; dummy dev accounts belong in `context.local.md`.
3. **State Boundaries:** Verify migrations before initiating build or release cycles.
