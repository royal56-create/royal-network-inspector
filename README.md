# Royal Network Inspector

A safety-first Nmap + Python toolkit for inspecting networks you own or are explicitly authorized to test.

## Features
- Private/loopback/link-local IP and CIDR validation; maximum 256 addresses per run
- Dry-run by default; real scans require both `--authorized` and `--execute`
- Nmap host discovery and conservative TCP top-100 service review
- XML parsing, result summaries, cautious informational risk hints
- JSON, CSV, and HTML reports; local scan history
- IP validation, subnet calculator, Nmap availability check
- Synthetic-data unit tests and GitHub Actions CI (no live scans in CI)

## Requirements
Python 3.10+. Nmap is required only for actual scans and must be available on PATH.

## Quick start
```bash
python main.py --help
python main.py validate 192.168.1.10
python main.py subnet 192.168.1.0/24
python main.py scan 192.168.1.10 --dry-run
```

For a permitted private lab host, preview first, then explicitly opt in:
```bash
python main.py scan 192.168.1.10 --dry-run
python main.py scan 192.168.1.10 --authorized --execute --format html
python main.py discover 192.168.1.0/24 --authorized --execute
```

## Commands
- `scan TARGET`: conservative TCP top-100 port/service review
- `discover TARGET_OR_CIDR`: host discovery only
- `validate IP_OR_CIDR`, `subnet CIDR`, `nmap-check`
- `analyze XML_FILE`: offline analysis of an existing XML file

Reports/history are local and may expose infrastructure details. They are excluded from Git. See [PROJECT_STATUS.md](PROJECT_STATUS.md), [docs/USER_GUIDE.md](docs/USER_GUIDE.md), [SECURITY.md](SECURITY.md), and [docs/LEGAL_AND_ETHICAL_USE.md](docs/LEGAL_AND_ETHICAL_USE.md).

**Safety boundary:** public targets, arbitrary Nmap flags, NSE scripts, exploitation, brute force, stealth/evasion, credential collection, and DoS features are intentionally unsupported. A private IP does not itself grant permission. Obtain documented authorization.

## Development
```bash
python -m unittest discover -s tests -v
python -m compileall -q src main.py
```
CI uses synthetic fixtures only; it never scans a real network. MIT License.
