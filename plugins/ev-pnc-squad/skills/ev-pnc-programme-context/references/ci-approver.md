# CI approver (merge gate) reference

Source: `EV_PNC_infra-modules`, `.github/workflows/ci-approver.yml`, policy in `auditor/approve.py`, tests in `auditor/tests/test_approve.py`, full README in `auditor/README.md` there. This note is the squad's working summary; if it disagrees with the repository, the repository wins.

## Where it sits
`auditor.yml` in each repository runs `audit` (gitleaks and repository audit), then `approve`, on every pull request (`opened`, `synchronize`, `reopened`, `ready_for_review`). `approve` reads the PR through the API, never checks out its code, publishes the **`ci-approver` commit status**, and merges on approve (squash by default, pinned to the judged head SHA). The verdict is a status, not a GitHub review: the PR author cannot approve their own PR.

## Verdicts
| Verdict | Status | When |
|---|---|---|
| approve | success, then merge | every check on the head commit green or skipped; no sensitive path; at most 100 files and 3000 lines; trusted author (default `COPUR`); no open review thread |
| wait | pending | other checks still running; the job polls up to 15 minutes, then holds |
| hold | pending | draft; base is not the default branch (stacked); fork; label `hold`, `do-not-merge` or `needs-human`; sensitive path; size limit; diff too large to inspect; test file deleted or a test disabled; unresolved thread |
| block | failure | failed check or status; merge conflict; changes requested; conflict marker or private key in the diff |

Sensitive paths always need a human: `.github/workflows/*`, `.github/actions/*`, `CODEOWNERS`, `.github/dependabot.yml`, `.gitleaks.toml`, `.auditor-allow`, `auditor/*`, `*.tf`, `*.tfvars`, `*Dockerfile*`. They are the control plane; a PR that edits CI or the secret scanner cannot approve itself.

## Merge order
1. `EV_PNC_infra-modules` first, with a **merge commit** (squash would orphan the commits callers pin).
2. Bump each caller's `uses:` and `auditor-ref:` / `approver-ref:` to the hub's new `main` commit; wait for the auditor to re-run green.
3. Callers next, independent of each other. Private repositories whose Actions cannot run (billing) have no green gate: hold them, never merge on a missing check.
4. Stacked PRs bottom first: merge the base PR, retarget the next PR to `main`, wait for its checks, merge, repeat.
5. The first rollout PRs change workflows, so the approver holds them; merging them is a human-authorised, hand-applied pass of the same policy.

## What only the repository owner can change
- Branch protection on `main`: required checks `audit / gitleaks`, `audit / repository audit`, `ci-approver`; CODEOWNERS review for `.github/`. Without it a collaborator can still merge by hand or edit the caller to drop the gate.
- Actions billing for private repositories (`EV_PNC_infra`, `EV_PnC_Consent_infra`).
- Repository settings such as automatic branch deletion.
