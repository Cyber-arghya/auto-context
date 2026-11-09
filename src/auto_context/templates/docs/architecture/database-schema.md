# Architecture: Database Schema & Data Models

## Overview
Database schema definitions, storage layout, entity relationships, and migrations for {{PROJECT_NAME}}.

## Entity Relationship Overview
```mermaid
erDiagram
    ACCOUNT ||--o{ SESSION : has
    ACCOUNT {
        string id PK
        string email UK
        datetime created_at
    }
    SESSION {
        string id PK
        string account_id FK
        datetime expires_at
    }
```

## Migration & Data Invariants
1. **Idempotency:** Schema migrations must execute deterministically without data duplication or side-effects.
2. **Zero Plaintext Secrets:** Passwords, private keys, and tokens must be securely hashed and never stored in raw text.
