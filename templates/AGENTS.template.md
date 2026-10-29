# Standing Agent Rules for {{PROJECT_NAME}}

## Critical Mandate: Autonomous `context.md` Synchronization
As an AI coding assistant working in this repository (`{{PROJECT_DIR}}`), you are **strictly mandated** to keep `{{PROJECT_DIR}}/context.md` continuously up to date. The user must **never** need to remind or instruct you to update it.

### 1. Mandatory Post-Action Protocol
Whenever ANY of the following events occur in any session or conversation turn:
- A configuration file or script is created, edited, moved, or deleted.
- A problem, bug, or error is encountered and diagnosed.
- Credentials, tokens, user accounts, or security keys are generated or updated.
- Architectural decisions or operational steps are modified.

**You MUST immediately update `{{PROJECT_DIR}}/context.md` before finalizing your response.**

### 2. Required Content & Structure in `context.md`
1. **Master Credentials & Configuration Vault (Section 1):** Keep all ports, IPs, secrets, tokens, and endpoints synchronized.
2. **Chronological Problem Log & Technical Solutions (Section 2):** Document symptom, root cause, exact commands/code used, and update Mermaid diagram.
3. **Architecture & Component Layout (Section 3):** Keep stack overview and directory maps accurate.
4. **Operations Runbook (Section 4):** Ensure 1-step reproduction instructions remain functional.
