# Project Status & Decision Log

- Project: Royal Network Inspector
- Portfolio sequence: 07/08
- Stack: Python + Nmap
- Repository: https://github.com/royal56-create/royal-network-inspector
- Release target: 1.0.0

## Agreed feature scope
Private-lab host discovery, bounded TCP port/service inspection, Nmap XML parsing, result analysis, JSON/CSV/HTML reporting, local history, IP/CIDR validation, subnet calculator, Nmap availability check, modular code, documentation, synthetic tests, and GitHub Actions CI.

## Fixed safety decisions
1. Dry-run is default. Real scans require both `--authorized` and `--execute`.
2. Only private, loopback, or link-local targets are accepted. Permission is still required.
3. Maximum 256 addresses per invocation.
4. Fixed argument profiles only; no shell execution or arbitrary Nmap flags.
5. Profiles: host discovery (`-sn -T2`) and conservative TCP top-100 service review (`-sV --version-light --top-ports 100 -T2`).
6. No NSE vulnerability scripts, exploitation, brute force, credential capture, stealth/evasion, or DoS.
7. Tests and CI use synthetic data only.
8. Local reports/history are ignored by Git.

## Work log — 2026-11-21
- Repository URL received and verified as an existing public repository.
- Version 1.0 scope converted into the initial project structure.
- Uploaded the initial Python package, CLI, documentation, sample XML, tests, and GitHub Actions workflow.
- Added JSON/CSV/HTML reporting, local scan-history support, and safety checks.

## Verification
GitHub Actions run #11 (commit `56da4477c10096059f9bdc1a8082899a26e27993`) completed successfully on 2026-11-21. Python compilation passed and all 9 synthetic unit tests passed. An earlier run exposed a discovery-mode XML-output mismatch; the command was corrected to use `-oX -`, and the follow-up run passed. No live network scan was performed by CI.

## Future backlog (not part of initial scope)
Signed release artifacts, offline report visualizations, and more synthetic XML edge-case fixtures.
