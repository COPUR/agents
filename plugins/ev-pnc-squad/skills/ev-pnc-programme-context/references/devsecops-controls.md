# DevSecOps controls for EV_PNC

Method: use the `ci-cd-and-devops` pipeline principles (build once and promote, fast feedback, pipeline as code, gates only where they earn their cost) and `api-design-and-security` for APIs. Scope comes from the epic's repositories.

## Programme-specific risks to cover
| Area | Why it matters here | Control to look for |
|---|---|---|
| Hub credentials | Hubject and GIREVE need certificates, OAuth2 clients, mTLS and CSR keys; onboarding takes about 3 months | Secrets in a key vault partition per environment, no secrets in repos or CI variables that fork PRs can read, rotation runbook (H-09) |
| Static egress | Hubs allow-list source IPs | Egress IPs in `EV_PNC_infra`, change through reviewed PRs only |
| Personal data | KVKK/GDPR: token UID, EMAID, trip traces, consent receipts | Encryption at rest and in transit, region pinning, retention jobs, no personal data in logs or test fixtures |
| Payments | No funds held; PSP tokens and pre-auth | Card data never touches own services (PSP tokenisation), PCI scope note in `EV_PNC_docs`, reconciliation alerts |
| Plug&Charge | Contract certificates, revocation | Private keys outside application containers, revocation path tested with the simulator |
| Public repos | Most EV_PNC_ repos are public | Secret scanning and push protection on, no internal hostnames or counsel text in commits, `infra` and consent infra stay private |
| Vendor contracts | Pinned Hubject and GIREVE contracts drift | Drift check in CI (H-01) with a failing job and an owner |
| Supply chain | Many small services, shared `ocpi-model` | Dependency and licence scan, lockfiles, pinned base images, SBOM per release, actions pinned to full SHA |

## Pipeline baseline (per repository)
1. Commit stage under 10 minutes: build, unit tests, lint, secret scan, dependency scan, packaging check; produce one versioned artefact tagged with the commit id.
2. Acceptance stage: deploy the same artefact to a production-like environment; run simulator-based end-to-end tests (P1-05); IaC scan; container image scan.
3. Release stage: promotion by configuration only; production behind a gate owned by a named role; smoke test asserts the deployed version.
4. Reusable workflows live in `EV_PNC_infra-modules` (P1-01); repositories call them rather than copying.
5. Workflow hardening: least-privilege `permissions`, no untrusted text in `run:`, fork PRs never see secrets, no self-hosted runners on public repositories, branch protection with required checks.
6. Rollback: feature toggle first, then fix forward or revert and re-run the full pipeline; database changes are expand then contract.

## Platform baseline
- Network policy default deny; hub adapters are the only workloads with hub egress.
- Workload identity instead of long-lived keys; RBAC reviewed per epic.
- Observability: logs, metrics, traces; SLOs for authorize latency and hub error rate; alert on outcomes. Dashboards for pilot KPIs belong to the Data agent.
- Backups and restore tested for consent and session data; incident playbook (S-02) names who speaks to whom.
- Threat model for the top flows (authorize, guest payment, hub onboarding, Plug&Charge) before the gate; STRIDE is enough.

## Findings format
Table: id, severity (critical, high, medium, low), repo, evidence (file, workflow, card), risk, fix, owner role, card to change or create. Separate Fact from Inference. A control you could not verify (private repo, no access) is listed as Unknown, never as passing.

## Boundaries
Do not run scanners against hub QA or production endpoints, and do not test third-party systems. Do not change production, rotate real secrets or edit workflows in a repository without the user's request for that change. Deployment and secrets changes that are hard to reverse wait for the product owner.
