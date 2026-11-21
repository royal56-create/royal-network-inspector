# Royal Network Inspector

A safety-first Nmap + Python toolkit for inspecting networks you own or are explicitly authorized to test.

## Features
- Private/loopback/link-local IP and CIDR validation; maximum 256 addresses per run
- Blocks public, multicast, reserved, and unspecified scan targets
- Dry-run by default; active operations require both `--authorized` and `--execute`
- Nmap host discovery and conservative TCP top-100 service review
- XML parsing, result summaries, cautious informational risk hints
- JSON, CSV, and HTML reports; local scan history
- DNS forward/reverse lookup and single-host TCP connectivity check
- DNS forward/reverse lookup, single-host TCP connectivity check, IP validation, subnet calculator, Nmap availability check
- Synthetic-data unit tests and GitHub Actions CI (no live scans in CI)

## Requirements
Python 3.10+. Nmap is required only for actual Nmap scans and must be available on PATH.

## Quick start
```bash
python main.py --help
python main.py validate 192.168.1.10
python main.py subnet 192.168.1.0/24
python main.py dns lab.local
python main.py scan 192.168.1.10 --dry-run
python main.py connect-check 192.168.1.10 443
```

For an authorized private lab host, preview first:
```bash
python main.py scan 192.168.1.10 --dry-run
python main.py scan 192.168.1.10 --authorized --execute --format html
python main.py discover 192.168.1.0/24 --authorized --execute
python main.py connect-check 192.168.1.10 443 --authorized --execute
```

## Commands
- `scan TARGET`: conservative TCP top-100 service review
- `discover TARGET_OR_CIDR`: host discovery only
- `dns NAME_OR_IP`: system-resolver A/AAAA or reverse PTR lookup
- `connect-check IP PORT`: one TCP connection check; preview-only by default
- `dns NAME_OR_IP`: forward A/AAAA or reverse PTR lookup
- `connect-check IP PORT`: one TCP connection check; preview-only by default
- `validate IP_OR_CIDR`, `subnet CIDR`, `nmap-check`
- `analyze XML_FILE`: offline analysis of an existing Nmap XML file

Reports/history are local and may expose infrastructure details. They are excluded from Git. See [PROJECT_STATUS.md](PROJECT_STATUS.md), [docs/USER_GUIDE.md](docs/USER_GUIDE.md), [SECURITY.md](SECURITY.md), and [docs/LEGAL_AND_ETHICAL_USE.md](docs/LEGAL_AND_ETHICAL_USE.md).

**Safety boundary:** public-target scans, arbitrary Nmap flags, NSE scripts, exploitation, brute force, stealth/evasion, credential collection, and DoS features are intentionally unsupported. DNS lookup is a normal resolver query. A private IP does not itself grant permission. Obtain documented authorization for active checks.

## Educational use, safety and responsibility

This repository is provided for educational, demonstration, and informational purposes. Review code and commands before use. Use it only with files, devices, repositories, and networks you own or are explicitly authorized to access. You are responsible for keeping backups, protecting personal information, and following applicable laws and policies. Use is at your own risk. The project is provided “as is” without warranties, to the maximum extent permitted by applicable law. Nothing in this notice excludes liability, rights, or obligations that cannot legally be excluded. This notice does not grant permission to access or test third-party systems.
