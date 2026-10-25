# Epic and channel map

Generated from `kanban/epics/` on 2026-10-25 (Slack workspace `copur`). Counts are all cards in the epic, including Done, Parked and Superseded. Regenerate from the CSV before relying on them after the board changes. Epic membership is a judgement layered on the v2 board, not part of it.

| Epic | Channel (id) | Cards | Roles | Main repositories |
|---|---|---|---|---|
| E0 Program governance and gates | #ev-pnc-program (`C0CBZCFHVA6`) | 27 | Architect, Compliance, Product owner | `EV_PNC_docs`, `all`, `EV_PNC_hub-contracts`, `EV_PNC_national-data`, `EV_PnC_Consent_docs` |
| E1 Legal, compliance and consent | #ev-pnc-e1-legal-consent (`C0CBU990F8V`) | 27 | Architect, Backend, Compliance, DevOps, Product owner, QA | `EV_PNC_docs`, `EV_PnC_Consent_registry`, `EV_PnC_Consent_docs`, `EV_PnC_Consent_notices`, `EV_PnC_Consent_decision` |
| E2 Roaming hubs: Hubject and GIREVE | #ev-pnc-e2-roaming-hubs (`C0CBU993F4M`) | 40 | Architect, Backend, BizDev, Compliance, DevOps, Product owner, QA | `EV_PNC_docs`, `EV_PNC_hub-gateway`, `EV_PNC_infra`, `EV_PNC_hub-contracts`, `EV_PNC_simulator` |
| E3 OCPI eMSP core platform and infra | #ev-pnc-e3-ocpi-platform (`C0CBXK2DJ86`) | 20 | Architect, Backend, DevOps, Product owner, QA | `EV_PNC_ocpi-emsp`, `EV_PNC_docs`, `EV_PNC_infra-modules`, `EV_PNC_infra`, `EV_PNC_simulator` |
| E4 Plug&Charge, payments and policy | #ev-pnc-e4-pnc-payments (`C0CC1EWTW8Z`) | 19 | Architect, Backend, BizDev, DevOps, Product owner, QA | `EV_PNC_docs`, `EV_PNC_payments`, `EV_PNC_plugcharge`, `EV_PNC_policy-engine`, `EV_PNC_pricing` |
| E5 Mobile app and route planner | #ev-pnc-e5-mobile-planner (`C0CC38YR00L`) | 11 | Mobile, Planner, Product owner, QA | `EV_PNC_mobile`, `EV_PNC_planner` |
| E6 Corridor pilot, KPIs and launch | #ev-pnc-e6-corridor-pilot (`C0CC38YU7S8`) | 33 | Backend, BizDev, Data, DevOps, Mobile, Planner, Product owner, QA | `EV_PNC_docs`, `EV_PNC_telemetry`, `EV_PNC_pilot-analytics`, `EV_PNC_planner`, `EV_PNC_mobile` |
| E7 National enabler (EPDK and e-Devlet) | #ev-pnc-e7-national-enabler (`C0CBJ6SP3HV`) | 13 | Architect, Backend, BizDev, Compliance, Product owner | `EV_PNC_docs`, `EV_PNC_national-data`, `EV_PNC_national-consent`, `EV_PNC_telemetry` |

## Goals and open human gates

**E0** Program governance and gates. Goal: Run the programme: decisions made on time, one weekly truth report, gate K1-K9 decided on 7 Dec 2026. Open human-gate cards: P0-01, P0-03, P0-18, R-02, S-03, G-01, G-02, G-04, G-05, S-02.

**E1** Legal, compliance and consent. Goal: K4 and K5 answered, KVKK basis signed off, consent family built; no hub contract signed while a blocker is open. Open human-gate cards: P0-04, TR-01, TR-02, TR-03, TR-04, TR-05, TR-23, K-01, K-15, K-02, P2-12, K-13.

**E2** Roaming hubs: Hubject and GIREVE. Goal: Hubject and GIREVE onboarding started in week 0; mock hubs green (K9); Plug&Charge via hub-managed path only if K2/K3 pass. Open human-gate cards: TR-08, TR-09, TR-13, TR-14, TR-19, TR-22, H-15, H-10, P5-02, TR-15, TR-27.

**E3** OCPI eMSP core platform and infra. Goal: Canonical OCPI model, simulator, CI/CD, real-time authorize, first real session with one CPO (P1-16). Open human-gate cards: P1-16.

**E4** Plug&Charge, payments and policy. Goal: Money flow without holding funds, PSP pre-auth/capture, guest flow, policy enforcement, managed contract certificates. Open human-gate cards: TR-06, P2-13.

**E5** Mobile app and route planner. Goal: Charge-stop optimiser plus mobile/CarPlay/Android Auto screens; Turkey beta. Open human-gate cards: P3-08.

**E6** Corridor pilot, KPIs and launch. Goal: Istanbul-Bodrum data foundation, KPI-1..7 baselines, pilot cohort, results report, hardening and launch. Open human-gate cards: P0-10, P0-12, C-17, P4-01, P4-03, P4-04, P4-06, C-13, C-16, C-19, P6-03, P6-04.

**E7** National enabler (EPDK and e-Devlet). Goal: Capped advocacy and reference-build track; moves only when EPDK or e-Devlet replies (N-08). Open human-gate cards: P0-06, P0-21, P0-07, N-01, N-08, N-07.

## Using the map

- BDAT scope for an epic = its cards' repositories plus the components they depend on in `repo-plan/v2/components.csv`.
- DevSecOps scope = the same repositories' pipelines and environments (`EV_PNC_infra-modules`, `EV_PNC_infra`, `EV_PnC_Consent_infra`) plus the secrets and hub-facing egress they use.
- Quality scope = the epic's acceptance criteria (card bodies), the matching `acceptance/*.feature` files and `traceability.csv`.
- `all` in the Repository column means a cross-cutting card; treat it as touching every repository of the epic that owns it.
- Wave-1 repositories exist (10 EV_PNC_ and 6 EV_PnC_Consent_); wave-2 repositories start after the gate or when their first card is pulled. Check that a repository exists before reading it.
