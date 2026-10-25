# Quality strategy for EV_PNC

Method: follow the `test-strategy` procedure (risk inventory, test shape, good-test rules, non-functional tests, data, CI gates, acceptance evidence) and `software-testing` for test design. Coverage percentages are not the goal; evidence for gates and KPIs is.

## Risk map (starting point, re-rank per request)
| Flow | Likelihood | Impact | Level |
|---|---|---|---|
| Real-time authorize with policy hook and consent gate | medium | high (wrong charge or refusal) | unit, contract, simulator e2e |
| Guest AD_HOC_USER pre-auth, capture on CDR, price formula | medium | high (money, K8 ceiling) | unit on pricing, PSP sandbox integration, reconciliation test |
| Hub adapters (Hubject OICP/OPCP, GIREVE OCPI/PNCP) | high | high | contract tests against pinned contracts, mock hubs with failure injection (K9) |
| Plug&Charge contract lifecycle | high | medium (conditional on K2/K3) | simulator ISO 15118 flows, revocation and renewal cases |
| Consent, retention, data subject rights | medium | high (legal) | Gherkin from `roaming-consent/acceptance/`, testkit, retention job tests |
| Planner: total time = drive + charge + expected queue | medium | medium | property tests, golden trips, trip replays; accuracy against KPI-2 |
| Live occupancy freshness (15 minute rule) | high | high (KPI-7 70%) | ingest tests, staleness alarms, reconciliation with EPDK list |
| Pilot KPI jobs and control/treatment split | medium | high (decision quality) | recomputation on a fixed fixture, white-box review (C-19), sample-size check |

## Test shape
- Domain logic: many fast unit tests. Adapters and persistence: integration tests with real dependencies in containers.
- Service boundaries: consumer-driven contract tests on every `*-api` and on pinned hub contracts. Run `H-01` drift check on a schedule.
- End to end: only the three core flows (P0-16) through the simulator harness (P1-05).
- Simulators are consumed over the wire as images; hub mocks come from pinned contracts, not from memory.

## Non-functional
- Performance: authorize p95 and p99 targets agreed per card; load, soak and failure-injection runs on a schedule, trends reviewed weekly.
- Resilience: hub timeout, retry and failover behaviour per the flow failure tables in `roaming-hubs/`.
- Security tests are DevSecOps-owned; quality checks that they run and are not skipped.
- Data: privacy-safe synthetic fixtures; no real driver data in tests.

## Gate and KPI evidence
- Gherkin features in `acceptance/` link to requirement ids; `traceability.csv` must show no gaps for the epic (runbook-checked requirements need no Gherkin). Use `roaming-hubs` `build_traceability.py` where present.
- KPI-1..7: check the formula, unit of measurement, period split (normal and peak), cell sizes. For proportions, about 96 observations per cell give plus or minus 10 points at 95%; there are five route families, so flag KPIs that cannot reach this (KPI-3 with fewer than 20 EVSE).
- Gates K1-K9: evidence must be re-runnable (command, data, date). Unverified user-supplied station facts are not K1 evidence.
- Definition of done: acceptance tests pass in CI, or evidence stored for human-gate cards. Definition of ready: acceptance criteria written, dependencies done or in the same iteration, repository exists, owner and gate flag set.

## CI gates
| Stage | Suites | Budget | Blocking |
|---|---|---|---|
| Commit | unit, lint, contract (local), packaging check | 10 min | yes |
| Merge | integration, simulator smoke | 20 min | yes |
| Nightly | full simulator e2e, drift check, soak | 2 h | alert and owner |
| Release | acceptance command set, version smoke test | 30 min | yes |

Flaky tests: quarantine with an owner and a deadline, never silent retries, never delete a test to get green.

## Output
Test strategy (risk table, shape per component, non-functional table, CI gates, acceptance evidence with the exact commands, gaps and accepted risks) or an audit with measured run time, flake rate and sampled smells. Report counts you ran, not counts you expect.
