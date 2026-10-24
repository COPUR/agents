# Hubject seed notes (retrieved 2026-10-24)

Re-verify against the sources in `source-registry.md` before relying on any line.

## Model

Hubject runs a central brokering system (HBS, sold as intercharge). EMPs and CPOs each connect once to the HBS. The HBS holds contracts, routes authorization, stores EVSE and pricing data, and forwards charge detail records (CDRs). Protocol: **OICP**, REST/JSON in 2.3 (SOAP existed up to 2.2).

## OICP 2.3 operation map (from the EMP and CPO OpenAPI files)

Base URLs: QA `https://service-qa.hubject.com/api/oicp`, production `https://service.hubject.com/api/oicp`.

| Service (version) | Path | Direction |
|---|---|---|
| eRoamingAuthorization: authorize start / stop (2.1) | `/charging/v21/operators/{operatorID}/authorize/start`, `.../authorize/stop` | CPO to Hubject; Hubject to EMP when online |
| Remote start / stop (2.1) | `/charging/v21/providers/{providerID}/authorize-remote/start`, `.../stop` | EMP to Hubject to CPO |
| Charge detail record (2.2) | `/cdrmgmt/v22/operators/{operatorID}/charge-detail-record` | CPO to Hubject to EMP (online EMP) |
| Get CDRs (2.2) | `/cdrmgmt/v22/providers/{providerID}/get-charge-detail-records-request` | EMP pulls (offline EMP) |
| Authentication data push (2.1) | `/authdata/v21/providers/{providerID}/push-request` | EMP to Hubject (offline authorization whitelist) |
| Reservation (1.1) | `/reservation/v11/providers/{providerID}/reservation-start-request`, `.../reservation-stop-request` | EMP to Hubject to CPO, optional |
| EVSE data pull (2.3) / push (2.3) | `/evsepull/v23/providers/{providerID}/data-records`, `/evsepush/v23/operators/{operatorID}/data-records` | EMP pulls, CPO pushes |
| EVSE status pull / push (2.1) | `/evsepull/v21/providers/{providerID}/status-records`, `/evsepush/v21/operators/{operatorID}/status-records` | same |
| Dynamic pricing (1.0) | `/dynamicpricing/v10/.../pricing-products`, `.../evse-pricing` | CPO pushes, EMP pulls |
| Charging notifications (1.1) | `/notificationmgmt/v11/charging-notifications` | CPO to Hubject to EMP: Start, Progress (at least 5 minutes apart), End, Error |

## Key behaviours (OICP 2.2 PDF and 2.3 OpenAPI descriptions)

- **Online vs offline EMP.** Offline EMPs push authentication data and download CDRs. Online EMPs answer authorization in real time and receive CDRs directly.
- **Authorize start routing.** Hubject creates a SessionID, then (a) authorizes offline from pushed data, else (b) derives the EMP from an EvcoID (QR code, Plug&Charge) and forwards to it, else (c) broadcasts to every EMP under contract with the CPO and authorizes if any says yes. An EMP that cannot be reached counts as NotAuthorized.
- **Identity.** Every request carries a ProviderID or OperatorID. Hubject compares it with the partner's SSL client certificate and returns status 017 on mismatch. Sub-EMPs and sub-operators can be bundled under a hub partner and are addressed implicitly through EvcoID or EvseID.
- **Sessions.** SessionID is Hubject-generated and must be echoed on later calls.
- **Push ordering.** Push requests of the same operation must be sequential.
- **Release management.** Each OICP version is supported for two years; partners declare which version they run. OICP 2.1 was retired 2023-04-13; new implementations must use 2.3.
- **Contract gating.** Hubject only processes a service request if the EMP and CPO have a valid contract for that service.

## Plug&Charge (OPCP 1.0.0)

Open Plug&Charge Protocol, in production use since 2019, on ISO 15118-2 and the VDE application rule VDE-AR-E 2802-100-1. Components:

- **RCP** Root Certificate Pool: root certificates of all participating PKIs.
- **PCP** Provisioning Certificate Pool: OEMs publish per-vehicle provisioning certificates by PCID; MOs fetch by PCID. OEM access is limited by WMI (first three PCID characters).
- **CPS** Certificate Provisioning Service: signs contract data from MOs (own CA) or has the V2G MO CA generate it.
- **CCP** Contract Certificate Pool: holds signed contract data per PCID; supports several EMAIDs per vehicle. CPO or OEM backends fetch on a `certificateInstallationRequest`.
- **V2G PKI services** and **webhook service** for events.
- Auth: OAuth2 with JWT carrying role (CPO, MO, OEM, CPS), allowed APIs, and the EMAID prefix (country code plus provider ID) or WMI the client may touch. TLS 1.3 recommended.
- MO paths: "MO with own PKI" (calls CPS createSignedContractData) or "MO with V2G PKI" (generateSignedContractData).
- ISO 15118-20 is prepared (separate namespace) but 1.0.0 is -2.

## Onboarding and certification (public view)

- EMP onboarding goes through the Hubject portal and `support.hubject.com`; the public pages give no step list.
- Testing and certification (HTF) is marketed for EVSE, OEM and CPO; no public procedure, prerequisites or prices. Certification procedure PDFs exist on the download page.
- OCPI is **not** a general Hubject interface in the sources read. Hubject Financial Services accepts OCPI 2.2.1 CDRs only (Credentials, Versions, CDRs), after the CPO is onboarded to intercharge and pushes EVSEs over OICP.
- Premium Services Contract API (EMP side, NGP subscription and CPO contact data) is documented in `hubject/Premium-Services-Doc`.

## Unknowns to chase

OICP 2.3 Integration Guide content (file names not enumerated), OPCP API schemas (`reference/*.v1.json`), intercharge CHECK certification procedure PDFs, commercial terms, whether Hubject exposes OCPI for roaming.
