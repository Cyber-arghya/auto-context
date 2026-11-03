# auto-context — Project Goals & Architecture Decision Records (ADR)

## 1. North Star & Core Objective
Provide an autonomous, deterministic, and token-efficient context and instruction management protocol for AI coding assistants (Antigravity, Cursor, Claude Code, Copilot, Windsurf).

## 2. Core Architectural Invariants
1. **Hub & Satellite Progressive Disclosure:**
   - `.agents/context.md` serves solely as a compact executive dispatch hub (< 60 lines).
   - High-density domain details live in satellite files (`gotchas.md`, `routes.md`) and are loaded strictly on-demand.
2. **Zero Dead Logs (The Brutal Truth Filter):**
   - Prohibit dumping chronological bug diaries or solved error logs.
   - Retain technical root-cause invariants inside `.agents/context/gotchas.md`.
3. **Single Source of Truth (SSOT):**
   - All canonical templates, rules, and skills live strictly in `src/auto_context/templates/`.
   - Zero duplicate directory trees in the repository.
4. **Strict Idempotency ($f(f(x)) = f(x)$):**
   - Running context initialization or update commands repeatedly produces deterministic output without duplicating blocks.
