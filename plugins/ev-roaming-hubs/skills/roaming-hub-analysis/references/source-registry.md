# Source registry (seed)

**Access notes (2026-10-24, cloud session):** `git clone` of public GitHub repositories works and is the best way to read whole Hubject repos; `raw.githubusercontent.com` works for known paths; GitHub tree pages, the GitHub API and codeload zips were blocked. Vendor sites were readable through a page-reading fetch (long PDFs need offsets) but not by direct download. Re-check in your own environment.

Verified reachable on 2026-10-24 unless noted. Re-verify before use. "Authority" tells you how far to trust a source: primary (the hub or standard owner), secondary (vendor or integrator write-up), press.

## Hubject

| Source | URL | Authority | Notes |
|---|---|---|---|
| OICP repository | https://github.com/hubject/oicp | primary | OICP 2.3 current, 2.2 tagged v2.2, 2.1 retired 2023-04-13. CC BY-SA 4.0. Acceptable Use Policy v1-0 is linked from the README. |
| OICP EMP 2.3 OpenAPI | https://raw.githubusercontent.com/hubject/oicp-emp-2.3-api-doc/master/src/openapi.yaml | primary | Paths, QA and production base URLs. Rendered docs at https://hubject.github.io/oicp-emp-2.3-api-doc/ need JavaScript. |
| OICP CPO 2.3 OpenAPI | https://raw.githubusercontent.com/hubject/oicp-cpo-2.3-api-doc/master/src/openapi.yaml | primary | Same layout as the EMP file. |
| OICP 2.2 EMP and CPO PDFs | linked from https://www.hubject.com/company/download | primary | Also in `awesome-ev-charging/oicp/`. |
| OICP 2.3 Integration Guide | https://github.com/hubject/OICP23_Integration_Guide | primary | Folders 01_Overview, 02_Acceptable-Use-Policy, 03_Services, 04_Definitions. Tree pages are crawler-blocked; file names not enumerated. |
| OPCP 1.0.0 | https://github.com/hubject/opcp | primary | Raw docs under `OPCP-1.0.0/docs/`, component docs under `components/`. API schemas in `reference/*.v1.json`. |
| Hubject support centre | https://support.hubject.com/hc/en-us | primary | Category index fetched; article bodies mostly not fetched. |
| OCPI CDRs to Financial Services | https://support.hubject.com/hc/en-us/articles/21771079863837 | primary | OCPI 2.2.1, Credentials and Versions plus CDRs only. |
| Testing and certification | https://www.hubject.com/products/testing-facility | primary | Marketing page; no step list or prices. |
| Certification procedure PDFs | linked from the download page | primary | Not read in the first run. |

## GIREVE

| Source | URL | Authority | Notes |
|---|---|---|---|
| OCPI 2.2.1 Implementation Guide v1.5 | https://www.gireve.com/wp-content/uploads/2026/04/Gireve_Tech_OCPI-V2.2.1_ImplementationGuide_V1.5-_en.pdf | primary | Hub deviations, per-module rules. |
| OCPI 2.1.1 Implementation Guide 1.2.9 | https://www.gireve.com/wp-content/uploads/2026/04/Gireve_Tech_OCPI-V2.1.1_ImplementationGuide_1.2.9_en.pdf | primary | Older versions 1.2.3 and 1.2.8 also published. |
| PNCP Implementation Guide 1.2.0 | https://www.gireve.com/wp-content/uploads/2026/05/Gireve_Info_Cnx_PNCP-Implementation-Guide_1.2.0_en.pdf | primary | Plug&Charge trust platform. First run read it up to section 3.8.3.2 (the fetch was truncated). |
| eMIP material | GIREVE download page | primary | Not retrieved in the first run; locate and read. |
| Foundation interview (2020) | https://www.gireve.com/?p=41066 | primary (dated) | Says GIREVE has supported eMIP and OCPI since 2018. |

## e-clearing.net

| Source | URL | Authority | Notes |
|---|---|---|---|
| Company site | https://www.e-clearing.net/ | primary | Aachen, Germany. Roaming, Charge Club, NAP Access. Claims 620,000+ charge points, 1,800+ partners. |
| Customer portal | https://support.e-clearing.net/portal | gated or unreachable | Not reachable in the first run. Do not attempt to log in. |
| Platform growth article (2020) | https://www.electrive.net/2020/12/20/plattform-e-clearing-net-waechst-auf-100-000-ladepunkte/ | press | OCHP and OCPI, eCHS 2.0, GmbH since August 2020. |
| Hubject and Smartlab Plug&Charge (2021) | https://www.electrive.com/2021/09/20/hubject-smartlab-join-forces-for-plugcharge-eroaming | press | Business-level only. |

## Secondary

| Source | URL | Caution |
|---|---|---|
| Codibly roaming overview | https://codibly.com/blog/articles/ev-roaming-solutions | Places e-clearing.net in the Netherlands and calls it a non-profit, and says Hubject bridges to OCPI. The first two conflict with the company's own site, the third with Hubject's support article. Treat as unreliable. |
| Monta eMIP article | https://monta.com/en/blog/emip/ | Generic; no GIREVE specifics. |
