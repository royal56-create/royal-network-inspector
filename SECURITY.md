# Security Policy

This toolkit is restricted to authorized private-lab learning. Scans require both `--authorized` and `--execute`; targets are limited to private, loopback, and link-local addresses and at most 256 addresses. Fixed Nmap arguments, subprocess argument arrays, and a timeout are used.

Not supported: exploitation, NSE scripts, brute force, credential collection, stealth/evasion, denial of service, or public-target scanning.

Report vulnerabilities through a private GitHub Security Advisory when available. Do not publish sensitive scan output, credentials, internal host inventories, or exploitable details in public issues.

These guardrails reduce risk but cannot prove authorization or guarantee a scan is harmless in every environment. Obtain permission from the network owner.
