---
name: roaming-hub-analysis
description: Reconstruct how EV roaming hubs (Hubject, GIREVE, e-clearing.net) work from public sources, and compare them with an OCPI eMSP. Use when planning hub connectivity, Plug&Charge contract-certificate flows (ISO 15118, OPCP, PNCP), OICP or eMIP translation, or hub onboarding and certification.
---

# Roaming hub analysis

Reconstruct a hub's protocols, flows and onboarding from what the hub publishes, then compare it with your own eMSP. Public sources only.

## Rules of engagement

- Allowed: public specs, public GitHub repositories, openly downloadable PDFs, public product, pricing and onboarding pages.
- Not allowed: logging in, using credentials, opening gated portals, calling hub QA or production APIs, capturing hub traffic, ignoring robots.txt or terms of service.
- A refused fetch is a finding. Record it and name the sanctioned route (the hub's onboarding contact).
- Respect licences: OICP and OPCP are CC BY-SA 4.0. Link and summarise; keep quotes short.

## Procedure

1. **Scope.** Hubs, role (eMSP, CPO or both), protocol versions, baseline. Read the baseline's version and modules from its repository.
2. **Source registry.** For each hub list URL, title, version, retrieved date, licence and authority (primary, vendor summary, press). Start from `references/source-registry.md`. Stop using a source that cannot be reached; do not paraphrase it from memory.
3. **Extract** per hub into `references/report-template.md`: protocol and module map, identity and security, message flows, Plug&Charge, onboarding and certification, commercial model, limitations.
4. **Tag every claim** Fact (cite), Inference (state the premise) or Unknown (name who can answer). Sources that conflict go in a "Conflicts" table with the more authoritative one marked.
5. **Diagram** each key flow as Mermaid `sequenceDiagram`. Use only participants and messages the sources show. Mark assumed steps with a `Note` containing "(assumed)".
5a. **Flow catalogue: happy and failure.** For every flow (registration, authorize, remote start and stop, notifications, session, CDR, data pull, Plug&Charge) record the happy path and a failure table, per `references/flows-guide.md`. Use only status codes, timeouts and retry rules the sources state.
6. **Gap analysis.** Compare to the baseline eMSP module by module. Each gap gets severity (blocker, needed for the pilot, later), an owner and a source.
7. **Repository needs.** Turn the gaps into a short list for the hub-connector repository: adapters, translators, test suites, configuration, runbooks.
8. **Open questions.** One list per hub for its onboarding team. Include everything you could not verify.
9. **Spec bundle.** Emit the spec-driven-development artifacts in `references/sdd-artifacts.md`: per-hub spec, plan, data model, contracts (pinned OpenAPI and AsyncAPI where the hub publishes them, overlay profiles where it only publishes PDFs), Gherkin acceptance files (tag `@happy` or `@error`), tasks, a traceability CSV and ADRs. Run `scripts/fetch_public_contracts.py` for the pinned contracts; do not retype published schemas. Lint each contract and report the result.

## Where to look, by hub

| Hub | Primary public sources | Notes |
|---|---|---|
| Hubject | `github.com/hubject` (clone the repos) (oicp, oicp-emp-2.3-api-doc, oicp-cpo-2.3-api-doc, opcp, OICP23_Integration_Guide), the documentation download page, `support.hubject.com` | OpenAPI sources are readable as raw files even where GitHub tree pages disallow crawlers. |
| GIREVE | Implementation guides on `gireve.com` (OCPI 2.1.1, 2.2.1, PNCP), eMIP material on its download page | The guides describe hub-specific deviations, which matter more than the base protocol. |
| e-clearing.net | Company site, press coverage, partner announcements | Little technical documentation is public; most is in a customer portal. Expect many Unknowns. |

`references/hubject.md`, `references/gireve.md` and `references/e-clearing.md` hold dated seed notes from a previous run. Use them to know what to look for. Re-check before relying on them, and update them when a source changes.

## Gap checklist for an OCPI 2.3.0 eMSP

- Version support: which OCPI versions the hub accepts. Hubs often lag the latest spec.
- Roles and registration: who initiates the credentials handshake, whether credentials can be updated, party IDs the hub exposes.
- Message routing: `OCPI-to-` and `OCPI-from-` headers, correlation IDs, one handshake for many parties.
- Modules: locations, tariffs, tokens, commands, sessions, CDRs, and which are one-way or unsupported. Check HubClientInfo, charging profiles, payments.
- Tokens: push versus real-time authorize, EMAID handling, UID format rules, `whitelist` semantics.
- Plug&Charge: contract-certificate path (EMAID, PCID, CPS, pools), root trust, who signs.
- Identity and transport: mTLS or token, IP allow-lists, certificate issuance.
- Data quality: static data review delays, required fields beyond the base spec.
- Tariff model: which tariff types are forwarded, per-eMSP pricing, rounding and VAT.
- Settlement: who rates the CDR, who clears, fees, dispute handling.
- Test and certification: sandbox, test suites, sign-off, how long it takes.

## Output

Two things per run: a Markdown report built from `references/report-template.md` (source registry at the end, dated, baseline version stated), and the spec bundle from `references/sdd-artifacts.md`. Only fact-based pilot requirements enter the specs; unknowns, inferences and deferred items go to `analysis/backlog.md` with the work package that would close them (`analysis/plan.md`).
