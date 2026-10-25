# BDAT views for EV_PNC

**BDAT is read here as the four TOGAF architecture domains: Business, Data, Application, Technology.** The project files never define the abbreviation, so this is an assumption. If the user means something else, stop and ask before producing artefacts.

Method: for the epic or card in scope, describe each view, then check the links between views. Follow the `architecture-review` procedure (ranked characteristics, options compared, risks, fitness functions, ADRs) when a decision is open, and the C4 and PlantUML sources in `engineering-briefing/uml/` when a diagram exists. Reuse numbering of existing ADRs (ADR-001 money flow, ADR-0006 guest price formula, ADR-0007 consent layers); never renumber.

## Business view
- Actors and roles: driver (registered, AD_HOC_USER guest, tourist), eMSP (the platform; neither CPO nor payment institution), CPO, roaming hub (Hubject, GIREVE, e-clearing.net), PSP, EPDK, e-Devlet (parked), counsel, DPO.
- Capabilities and value streams: plan trip, authorize, charge, settle (CDR to payment), roam, consent, measure pilot.
- Money and legal flow: B2B cost + fixed margin + VAT, TL/kWh only; funds are never held. Check each change against K4 (resale, KVKK transfer basis) and K5 (provider ID, EMAID prefix).
- Check: every capability maps to a card, an owner role and a KPI or gate. Unowned capabilities are findings.

## Data view
- Entities and owners: token UID, EMAID, session, CDR, tariff, price, consent receipt, vehicle binding (VIN and registration document), location trace, KPI event.
- For each entity: system of record, classification (personal under KVKK/GDPR, payment, public), retention (location traces reduce to H3 resolution 8 cells after 90 days per `CP-KPI-004`), cross-border flow (Germany, France hubs) and legal basis (standard contract for roaming, not consent).
- Consistency: authorize is real-time; CDRs reconcile later; pilot KPIs use pseudonymous trip ids. Name where eventual consistency is acceptable.
- Check: no personal field appears in two systems of record; every transfer has a basis in the KVKK matrix (K-01) or is flagged Unknown.

## Application view
- Components and contracts come from `repo-plan/v2/components.csv`: `ocpi-model` and each `*-api` (stable, abstract), deployables (`ocpi-emsp`, `policy-server`, `pricing-server`, `payments-server`, `plugcharge-server`, `telemetry-server`, `planner-server`, hub adapters, `api-gateway-server`), apps, test tooling.
- Rules: deployables depend on `*-api` and `ocpi-model`, never on another deployable; no cycles (run `tools/packaging_check.py --strict` from `repo-plan/v2/`); hubs sit behind canonical ports; simulators are consumed over the wire.
- Spec reminders: no Bookings module in OCPI 2.3.0; StartSession goes eMSP to CPO; real-time authorize instead of pushing EMAID tokens; hub profiles map 2.3.0 to 2.2.1.
- Check: each interaction states sync or async, idempotency key, timeout and retry rule, and the failure a caller sees.

## Technology view
- Hosting in a Turkey region (K8s base, E3), reusable Terraform modules and Helm charts (`infra-modules`), private environments (`infra`), key vault partitions, static egress IPs and hub allow-lists, observability.
- Hub-facing needs: mTLS and OAuth2 for PNCP, certificate and key handling, allow-listed egress. Plug&Charge PKI is a spike (P0-08); do not design own PKI/HSM (parked).
- Check: each application component names its runtime, scaling unit, data store, secret source and SLO. Hand pipeline and control design to the DevSecOps agent and test design to the quality agent.

## Cross-view checks (the part that finds problems)
1. Business capability without an application component, or a component without a capability.
2. Personal data in the Data view without a Technology control (encryption, retention job, region).
3. A Business promise (zero-interaction Plug&Charge) that depends on a conditional gate (K2/K3): mark it conditional.
4. Dependencies that cross epics: list the card pair and who waits.

## Output
Use the architecture-review template, trimmed to the scope: summary and recommendation, four views (a table each, diagram only where the flow is the point), cross-view findings, options and trade-offs for open decisions, fitness functions, ADR drafts, open questions. Put drafts under the repository named by the card (usually `EV_PNC_docs`); do not push to it unless asked.
