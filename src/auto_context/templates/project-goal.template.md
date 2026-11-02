# 🎯 {{PROJECT_NAME}} — Project Goals, North Star & Architecture Decision Records (ADR)

> **Last Updated:** {{DATE_NOW}} | **Status:** Active Development  
> **Stack:** {{STACK}} ({{FRAMEWORK}}) | **Purpose:** Strategic North Star & Product Decision Gatekeeper

---

## 1. The "Why" & Target Audience
- **Core Purpose:** What real-world problem does this project solve? Why was it created?
- **Target Audience:** Who will use this application/tool and what pain points does it eliminate?
- **Unique Value Proposition (UVP):** What makes this project distinctly better or different from existing alternatives?

---

## 2. Active Roadmap & Current Phase
- **Current Milestone:** Phase 1 — Core Foundation & MVP
- **Immediate Next Priorities:**
  1. Priority 1: Core functionality implementation
  2. Priority 2: Rigorous verification & test coverage
  3. Priority 3: Developer documentation & clean interface

---

## 3. Anti-Goals & Out-of-Scope (What We Will NEVER Build)
<!-- Explicit constraints to prevent feature creep and unnecessary bloat -->
- [ ] No feature bloat or over-engineering that distracts from the core purpose.
- [ ] No monolithic state or tight coupling that violates modular DRY/KISS architecture.

---

## 4. Architectural Decisions & Tradeoffs (ADR)
<!-- Record all key technical and architectural decisions: why chosen vs alternative -->

| Decision | Chosen Approach | Rejected Alternative | Why (Technical / Business Rationale) |
| :--- | :--- | :--- | :--- |
| **Architecture** | Modular & KISS | Monolithic / Complex | Preserves token efficiency, maintainability, and clean boundaries. |

---

## 5. Idea Validation & Brutal Truth Filter Checklist
Before proposing or accepting any new feature, verify against this checklist:
- [ ] **Alignment:** Does this feature directly advance the current milestone?
- [ ] **Simplicity:** Is there an industry-standard simpler way to achieve this?
- [ ] **Worth-It Test:** Does it pass "The Brutal Truth Filter" (is the value worth the added code and maintenance cost)?
- [ ] **Deviation Rationale:** If deviating from standard industry practices, is the specific reason documented in Section 4 above?

