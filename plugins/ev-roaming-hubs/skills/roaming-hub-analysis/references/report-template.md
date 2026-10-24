# Roaming hub report: <hubs> — <date>

Baseline: <repo, version/commit, OCPI version, modules>.
Scope: <role, hubs, versions>. Sources: public only (see registry).

## 1. Summary
Three to six bullets: what each hub is, what the eMSP must build first, biggest unknowns.

## 2. Per hub (repeat for each)
### 2.1 Model and protocols
Table: layer, protocol, versions, transport, status.
### 2.2 Module map
Table: function (locations, tariffs, authorization, remote start, sessions/CDR, reservation, pricing, PnC) → protocol operation or module → direction → notes.
### 2.3 Identity and security
IDs, auth, certificates, IP rules, environments.
### 2.4 Message flows
One Mermaid sequence diagram per flow: authorize/start, CDR, data sync, PnC contract provisioning, PnC authorization.
### 2.5 Onboarding and certification
Numbered steps with source for each; list the steps that are not public.
### 2.6 Commercial model
What is stated, what is not.
### 2.7 Limitations and quirks

## 3. Conflicts between sources
Table: claim, source A, source B, resolution.

## 4. Gaps against the baseline eMSP
Table: area, hub requirement, baseline state, severity, owner, source.

## 5. What the hub-connector repository needs
Adapters, translators, test suites, config, runbooks. Group by hub.

## 6. Open questions per hub

## 7. Not verified
Everything unreachable, truncated or inferred.

## 8. Source registry
URL, title, version, retrieved, licence, authority.
