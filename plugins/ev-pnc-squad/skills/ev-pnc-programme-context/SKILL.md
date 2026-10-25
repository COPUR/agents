---
name: ev-pnc-programme-context
description: Shared context for the EV_PNC squad agents (BDAT architect, DevSecOps engineer, quality lead). Use when scoping work to the EV_PNC programme Slack channels, epics E0-E7, kanban v2 cards, repositories, gates K1-K9 or KPI-1..7.
---

# EV_PNC programme context

The EV_PNC programme builds a neutral Turkish eMSP (OCPI 2.3.0-shaped, hubs behind ports, Plug&Charge conditional) and runs an Istanbul-Bodrum corridor pilot. Work is organised as eight epics, one Slack channel each, over a 190-card kanban (v2, 25 Oct 2026). This skill is the map the three squad agents share. It is dated 2026-10-25: re-read the sources before relying on a count.

## Sources of truth, in order

1. `kanban/v2/ev_pnc_backlog_v2.csv` and `kanban/epics/ev_pnc_backlog_v2_with_epics.csv` (card ids are stable; the CSV wins over Slack).
2. The repository set plan `repo-plan/v2/` (`components.csv` has the component dependency graph) and the spec folders `corridor-pilot/`, `roaming-hubs/`, `roaming-consent/`, `national-hub-service/`, each with a `traceability.csv`.
3. The Slack channels, as the working view only. A card's status lives in its thread.

Project files sit in the project's shared folder; if the caller gave no path, ask where they are rather than guessing.

## Epic and channel map

`references/epic-channel-map.md` lists, per epic: channel name and id, goal, card count, owner roles, main repositories and gate cards. Load it before scoping a request. Rule: **a request names a channel, an epic (E0-E7) or a card id; resolve it to that epic's cards and repositories and stay inside them.** A card outside the named epic is a dependency to report, not a scope to widen.

## Slack rules

- Reading channels and threads is allowed. Prefer the CSV for card facts and use Slack for status, decisions and open questions.
- Never post, react, schedule or edit in Slack without the user's explicit go-ahead for that message. Draft the text and show it first.
- A scheduled read-only digest of the same channels already exists. Do not build another monitor or summary job; answer the question you were asked.
- Legal and negotiation content (E1, E2) is in public channels. Do not copy counsel questions, prices or hub terms into new places beyond what the task needs.

## Decision vocabulary the programme already uses

- Gates K1-K9 decide go or no-go on 7 Dec 2026 (G-04). Examples used by the agents: K1 corridor EVSE evidence, K2/K3 ISO 15118-2 readiness (at least 20 EVSE for K3), K4 resale and KVKK transfer basis, K5 TR provider ID and EMAID prefix, K8 guest price ceiling, K9 mock hubs green. Read `corridor-pilot/` and `roaming-hubs/deliverables/07-go-no-go.md` for the exact wording.
- KPI-1..7 are defined in `corridor-pilot/kpis.md` (wait time, trip-time deviation, Plug&Charge success, alternative uptake, guest conversion, power sharing, data coverage).
- Card status words: Ready, In progress, Blocked, Review, Done. WIP limit 6. At most 6 open product-owner gates.
- Fixed decisions: e-Devlet is parked (VIN and registration document instead); hubs behind canonical ports; no funds held; guest price in TL/kWh only; do not push EMAID tokens, use real-time authorize; OCPI 2.3.0 has no Bookings module; StartSession goes eMSP to CPO.

## Evidence rules shared by all three agents

- Tag claims Fact (cite file or card), Inference (say from what) or Unknown (say who can confirm). User-supplied station details are unverified and do not count as K1 evidence.
- A recommendation names its cost and the card it would change. New work means dropping a card (programme rule).
- Say which checks you could not run. Never mark a card Done: that needs CI evidence or a stored artefact, and the product owner decides gates.

## Where the role detail lives

- `references/bdat-views.md`: the four architecture views, per-view artefacts and checks.
- `references/devsecops-controls.md`: pipeline and platform controls, repo by repo.
- `references/quality-strategy.md`: risk map, test levels, KPI and gate evidence.
