# GIREVE seed notes (retrieved 2026-10-24)

Re-verify against `source-registry.md` before relying on any line.

## Model

GIREVE is a roaming platform ("IOP") that routes between operators and translates between protocols. It supports its own **eMIP** and **OCPI**. OCPI versions with published guides: 2.1.1 (guide 1.2.9) and 2.2.1 (guide 1.5). A separate trust platform serves Plug&Charge over **PNCP**.

## OCPI 2.2.1 on GIREVE (guide v1.5)

| Topic | Rule |
|---|---|
| Modules | Credentials, Locations, Tokens, Commands, Sessions, CDRs, Tariffs supported. ChargingProfiles not supported. HubClientInfo: the module table says not implemented while later sections list use cases. Ask. |
| Hub identity | Country code FR. Party ID 107 in pre-production, 007 in production. |
| Registration | Only "FromIOP" register and unregister. No credentials update: unregister, then register again. Operators are created manually by GIREVE after contracting. HTTPS required, IP filtering, GIREVE-issued client certificate mandatory. Authorization tokens must be Base64. |
| Routing | `OCPI-to-` and `OCPI-from-` headers mandatory except for credentials and versions. One handshake covers all parties a platform hosts. `X-Request-ID` and `X-Correlation-ID` required and echoed. |
| Locations | Extra required fields: owner name, operator name, connector tariff IDs, EVSE capabilities. Static data passes a quality process (hours of delay); dynamic data is real time. Plug&Charge is signalled through connector capabilities `ISO_15118_2_PLUG_AND_CHARGE` and `ISO_15118_20_PLUG_AND_CHARGE`. GIREVE adds a non-OCPI `gireve_id`. |
| Tokens | CPOs do not download eMSP tokens; they call `POST tokens/{uid}/authorize` for unknown tokens. eMSPs must push their full token list so OCPI 2.1.1 CPOs can roam. No PATCH to IOP, no pull from IOP. RFID UIDs uppercase hex, 4 or 7 bytes. |
| Commands | START_SESSION and STOP_SESSION only. `evse_uid` mandatory on start. Reserve, cancel and unlock not implemented. |
| Sessions | No PATCH on the IOP side, no smart charging. Meter updates at least two minutes apart. Session IDs replaced by GIREVE IDs. eMSPs cannot pull sessions. |
| CDRs | Sent immediately after session end. No credit CDRs. Remarks prefix shows who priced it. |
| Tariffs | Immutable except text and end date. Only "B2B Regular" tariffs forwarded to eMSPs. Per-eMSP pricing through `target_operator_*` fields. Extra dimension `SESSION_TIME`. |
| Reliability | Store and forward for sessions and CDRs with progressive back-off; no bursts. |
| VAT | Passed through as sent by the CPO, not computed. |
| Certification | The guide describes no formal certification path or sandbox scenarios. The 2.1.1 guide mentions a "standard GIREVE certification process" for Eichrecht signed data and a contact address for connection. |
| Commercial | Roaming agreements live on the Connect Place (GIREVE's marketplace). |

## PNCP (Plug&Charge trust platform), guide 1.2.0

- Scope: PKI services, V2G Root CA, Certificate Provisioning Service, and pools: CCP (contract), PCP (provisioning), RCP (root).
- Environments: preproduction `pp-trust-api`, production `trust-api`. URL pattern `https://<env>.gireve.com/pncp/<version>/<module>`. Modules: generic certificate, root CA, provisioning certificate, contract certificate.
- Conventions copied from OCPI: `X-Request-ID`, `X-Correlation-ID`, paging headers. Operator identified by `PNCP-from-country-code` and `PNCP-from-party-id`.
- Auth: OAuth2 bearer tokens from client ID and secret issued by GIREVE; TLS 1.3; IP filtering; HSM-protected CA keys; HMAC-SHA256 signed webhooks from one fixed IP.
- Keys and formats: ECDSA secp256r1; CSR PKCS#10 PEM; EST responses PKCS#7; ISO 15118-2 payloads EXI plus Base64.
- eMSP flow: create or enrol a contract certificate for an eMAID, fetch the vehicle's provisioning certificate by PCID, validate the chain against OEM roots from the RCP, build the contract certificate bundle, have the CPS sign it into an SCCB, store it in the CCP. Expiry warning webhook 50 days ahead.
- CPO or OEM flow: on `CertificateInstallationRequest`, fetch SCCBs by request (or by PCID for OEMs). GIREVE validates format, chain, expiry, revocation and signature, filters, and returns each result with an `owner_operator`; only one contract certificate can be installed in the EV at a time.
- Roaming authorization for PnC: OCPI `POST tokens/{uid}/authorize` with the eMAID in `auth_id` (type OTHER), or the eMIP GetServiceAuthorisation call with the eMAID as `userId`.
- Onboarding: GIREVE issues credentials, you supply machine IPs, an admin binds permissions per subscription, certificate profiles are agreed per operator (DN, validity, SubCA2), root CAs are submitted through secure file transfer, webhooks configured.

## Unknowns to chase

eMIP specification (not retrieved), PNCP guide after section 3.8.3.2, test environment access and qualification scenarios, Connect Place workflow, price list, HubClientInfo status, whether OCPI 2.3.0 is planned.
