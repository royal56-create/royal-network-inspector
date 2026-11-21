# Feature Inventory

## Included in version 1.0
- IP/CIDR validation with private, loopback, and link-local scope restrictions
- Blocks multicast, reserved, unspecified, and public targets from active checks
- Subnet calculator with a 256-address cap
- DNS A/AAAA lookup and reverse PTR lookup through the configured system resolver
- Single-IP TCP reachability check with preview-first behavior and explicit authorization
- Nmap host discovery and conservative TCP top-100 service detection
- Nmap XML parsing, summary analysis, JSON/CSV/HTML exports, and local scan history
- Offline XML analysis, CLI help, synthetic unit tests, and GitHub Actions CI

## Intentionally excluded
Public-target scanning, arbitrary Nmap options, NSE scripts, vulnerability exploitation, brute force, credential capture, stealth/evasion, denial-of-service testing, and broad port sweeps.

## Not yet included
MAC vendor/OUI database, OS fingerprinting, visual dashboard, signed release artifacts, and a graphical interface. These are not advertised as available features.
