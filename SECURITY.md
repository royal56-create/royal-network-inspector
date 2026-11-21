# Security Policy

This toolkit is restricted to authorized private-lab learning. Nmap scans and TCP connectivity checks require both `--authorized` and `--execute`; targets are limited to private, loopback, and link-local addresses, and Nmap ranges are capped at 256 addresses. A TCP connectivity check is limited to one IP and one port with a short timeout. DNS lookup uses the operating system's configured resolver.

Fixed Nmap argument profiles, subprocess argument arrays, and a timeout are used. Multicast, reserved, unspecified, and public targets are blocked for active checks.

Not supported: exploitation, NSE scripts, brute force, credential collection, stealth/evasion, denial of service, or broad port sweeps.

Report vulnerabilities through a private GitHub Security Advisory when available. Do not publish sensitive scan output, credentials, internal host inventories, or exploitable details in public issues.

These guardrails reduce risk but cannot prove authorization or guarantee a check is harmless in every environment. Obtain permission from the network owner.
## User responsibility and warranty notice

Use this project only for lawful learning and on resources you own or are explicitly authorized to use. Review all code and commands before running them, keep independent backups, and protect private data. Use is at your own risk. The project is supplied “as is” without warranties, to the maximum extent permitted by applicable law. Nothing here excludes non-waivable rights, liabilities, or obligations. An educational-purpose notice is not permission to access or test third-party systems.
