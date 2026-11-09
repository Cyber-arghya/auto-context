# Architecture: API Design & Route Contracts

## Overview
API route contracts, endpoints inventory, and input/output interfaces for {{PROJECT_NAME}}.

## Route Registry
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/api/health` | Service health and liveness probe | No |

## API Standards
1. **Response Envelope:** Use standard JSON schemas with deterministic error payloads: `{"error": "<message>", "code": "<ERROR_CODE>"}`.
2. **Input Validation:** Reject malformed request payloads at ingress boundaries prior to service invocation.
