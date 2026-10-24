# Flow catalogue: happy paths and failure flows

Write one `flows.md` per hub. Facts only; every code, timeout and retry rule needs a citation. Unknown behaviour is listed as Unknown with the question that closes it.

## Per flow

1. **Happy path.** Mermaid `sequenceDiagram` with only the participants and messages the sources show.
2. **Failure table.** One row per failure:

| Trigger | Detected by | Code or event (cite) | eMSP action | Retry or timeout | Customer effect |
|---|---|---|---|---|---|

3. **Scenarios.** One Gherkin scenario per row you can build against a mock, tagged `@happy` or `@error` plus the requirement id. Rows that need the hub sandbox get `@sandbox`; rows whose behaviour is not published get `@pending-confirmation` and live in the backlog, not the build spec.

## Failure classes to check for every flow

- Identity: unknown or blocked token, expired contract, ID or certificate mismatch.
- Availability: charge point unknown, offline or busy; hub or CPO unreachable.
- Time: authorize, command and session timeouts; late answers; hub-side close.
- Duplicates and loss: replayed or duplicate messages, lost CDRs, reconciliation.
- Throttling: rate limits and what the hub returns.
- Data rules: case sensitivity, placeholders, size limits, version mismatch.
- Credentials: expiry, rotation, key reuse, revoked certificates, signature failures.
- Our side: partial outage, slow policy decision, queue backlog.

## Charge point side

The hub documents usually stop at the CPO. Record charge-point behaviour (for example OCPP transaction and remote-control messages) only where the hub or a cited standard states it, and mark the rest Unknown.
