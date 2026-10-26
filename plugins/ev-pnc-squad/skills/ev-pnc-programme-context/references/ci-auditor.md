# CI auditor (shared workflow) reference

Source: `EV_PNC_infra-modules`, `.github/workflows/ci-auditor.yml`, scripts and tests in `auditor/`, full README in `auditor/README.md` there. This note is the squad's working summary; if it disagrees with the repository, the repository wins.

## What runs, on which events
Every repository calls the shared workflow from `.github/workflows/auditor.yml` on `push`, `pull_request`, a weekly `schedule` (full-history rescan) and `workflow_dispatch`. Two jobs:

| Job | Does | Fails on |
|---|---|---|
| `audit / gitleaks` | gitleaks v8.30.1 with the repository's `.gitleaks.toml` (default rules on) plus project rules: TCKN, card PAN, OCPI `Authorization: Token`, Kafka JAAS password. Range: PR commits, pushed range, or full history. | any finding |
| `audit / repository audit` | required files; gitleaks config not weakened; committed `.env`, state, keystore, SSH and kubeconfig files or private keys; files over 5 MiB; workflow hygiene; Dockerfile and Terraform warnings; `actionlint` | errors (warnings are reported) |

Workflow hygiene errors: no `permissions:`, `pull_request_target`, attacker-controlled `${{ }}` in `run:`. Unpinned third-party actions are warnings (errors with `strict-pinning`). `COPUR/*` callers are exempt from pinning.

## Caller shape (what coverage checks look for)
```yaml
jobs:
  audit:
    uses: COPUR/EV_PNC_infra-modules/.github/workflows/ci-auditor.yml@<full sha>
    with:
      public: true            # false for EV_PNC_infra and EV_PnC_Consent_infra
      auditor-ref: <same sha>
```
Both values must be the same commit; they pick the workflow file and the scripts it runs.

## Triage playbook
| Symptom | Likely cause | First move |
|---|---|---|
| `gitleaks` red on a default rule | real credential committed | Treat as leaked: rotate, then remove. Product owner decides history rewrite. |
| `gitleaks` red on a project rule in docs | example data that looks real (TCKN, PAN, token) | Replace with a placeholder or published test value; allowlist only if the text must stay, narrowly, in `.gitleaks.toml` |
| `forbidden-file` | state, keystore or `.env` committed | Remove, add to `.gitignore`, rotate if real; `.auditor-allow` only for reviewed fixtures |
| `workflow-script-injection` | `${{ github.head_ref }}` or PR title in `run:` | Pass through `env:` and quote the variable |
| `workflow-permissions` | no `permissions:` block | Add top-level `permissions: contents: read` |
| `actionlint` error | syntax or shellcheck issue | Fix at the line given |
| Job fails before the scan (checkout, `go install`) | infrastructure | Re-run once; if it repeats, read the step log and check the pinned versions |

## Open decisions (2026-10-26)
- Callers pin the hub by full SHA because tags cannot be pushed from the agent environment. After the hub PR merges, bump every caller to the merge commit on `main`, or create a `v1` tag and use it (then drop the `auditor-ref` pair).
- Required status checks in branch protection are not set by this rollout; settings are the product owner's.
- Forks and third-party repositories attached to the project (`ocpi`, `awesome-*`, `mcp_rea`, `awesome-claude-code-subagents`, `ai-agent-protocols`) are not covered.
