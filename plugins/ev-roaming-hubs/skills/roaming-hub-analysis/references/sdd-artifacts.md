# Spec-driven-development artifacts

The report is for people. The spec bundle is for the team (and coding agents) that will build the hub connector. Layout follows the common spec-kit shape (spec, plan, data model, contracts, tasks) so any SDD tool can read it.

```
roaming-hubs/
  README.md                     start here: what to read for what
  report.md                     the human report
  analysis/backlog.md           everything not build-ready (unknowns, inferences, deferred, blocked, questions)
  analysis/plan.md              deep-analysis work packages that close the backlog
  analysis/drafts/              inference-heavy drafts (mappings, unverified event payloads)
specs/roaming-hubs/
  README.md                     index, baseline version, how to regenerate
  traceability.csv              requirement → source → contract → test → task
  adr/NNNN-<title>.md           one decision per file
  _sources/                     pinned public contracts (generated, never hand-edited)
  <hub>/
    spec.md                     scope, actors, requirements, non-goals, open questions
    plan.md                     connector design against the baseline eMSP
    data-model.md               identifier and entity mapping (hub ↔ baseline)
    contracts/
      *.openapi.yaml|json       HTTP contracts the eMSP implements or calls
      *.asyncapi.yaml           webhooks and notification streams
      *.profile.yaml            hub deviations from a base protocol (overlay, see below)
      mapping-*.yaml            field-level translation tables
    acceptance/*.feature        Gherkin, one file per flow (happy and error scenarios)
    tasks.md                    ordered work items with dependencies and requirement IDs
```

## Requirements (spec.md)

ID: `RH-<HUB>-<AREA>-<NNN>`, for example `RH-HUBJECT-AUTH-003`. Areas: REG, AUTH, CMD, SESSION, CDR, LOC, TARIFF, PNC, SEC, OPS, CERT.

One line per requirement in EARS form, then metadata:

```
RH-GIREVE-TOK-002  WHEN the hub receives a token authorization for an unknown token
THE eMSP SHALL answer POST /tokens/{uid}/authorize in real time.
  source: <URL + section>   confidence: fact|inference|unknown   priority: pilot|later
  verify: acceptance/tokens.feature#real-time-authorize
```

**Build-ready rule.** A requirement goes into `spec.md` only if it is a cited fact (or an explicit project requirement) with pilot priority and has a task and an acceptance scenario. Unknowns, inferences, deferred items and blocked work go to `analysis/backlog.md` with the work package that would promote them. This keeps the specs unambiguous for whoever builds from them.

Rules: derive only from sources. `inference` needs the premise written out. `unknown` becomes an open question and a blocked task, never a guessed requirement. Use RFC 2119 words only where the source does.

## Contracts

- Prefer pinning what the hub publishes. `scripts/fetch_public_contracts.py` writes eMSP-role subsets with `x-source`, `x-retrieved` and `x-licence`. Do not retype published schemas.
- Where the hub publishes no machine-readable contract (PDF guides), write an **overlay profile**: YAML with `base` (protocol and version), `modules`, `headers`, `required_extra_fields`, `unsupported`, `limits`, `quirks`. Each entry carries `source` and `confidence`.
- Webhook or event streams go in AsyncAPI 2.6 or 3.0. Include the signature scheme if documented.
- Validate: `npx @redocly/cli lint <file>` for OpenAPI, `npx @asyncapi/cli validate <file>` for AsyncAPI, and a YAML parse for profiles. Report validation results in the README.
- Respect licences. OICP and OPCP derived files stay CC BY-SA 4.0 with attribution in the header.

## Acceptance (Gherkin)

One feature per flow. Steps use the baseline's vocabulary (OCPI objects) on one side and the hub's on the other. Tag each scenario `@happy` or `@error` and `@RH-...` with the requirement it proves and `@sandbox` when it can only run against the hub's test environment, `@mock` when a recorded or simulated hub is enough. No scenario may assume behaviour the sources do not state; tag those `@pending-confirmation`.

## Tasks

`T-<HUB>-NN | title | requirement IDs | depends on | environment (mock, hub sandbox, none) | exit check`. Blocked tasks name the open question they wait on.

## Traceability

Requirements checked by a runbook or onboarding checklist use `verify: runbook check (...)` and need no Gherkin. Run `scripts/build_traceability.py <specs dir>`; it writes the CSV and lists requirements missing a task or scenario, and acceptance tags with no requirement.


`traceability.csv` columns: `requirement_id,hub,area,priority,confidence,source_url,contract,acceptance,task,status`. Every requirement has a row; empty `acceptance` or `task` cells are gaps to report.

## ADRs

Record decisions the analysis forces (for example, translate OICP to OCPI at the edge, or run OICP as its own module). Format: context, decision, consequences, sources.
