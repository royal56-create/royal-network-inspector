# User Guide

## Safety model
Nmap scans and TCP connectivity checks default to preview-only. Active operations require both `--authorized` and `--execute`. Active targets must be private, loopback, or link-local; Nmap CIDR ranges are capped at 256 addresses. Obtain permission from the owner even for private networks.

## Examples
```bash
python main.py validate 192.168.1.10
python main.py subnet 192.168.1.0/24
python main.py dns lab.local
python main.py scan 192.168.1.10 --dry-run
python main.py discover 192.168.1.0/24 --dry-run
python main.py connect-check 192.168.1.10 443
python main.py connect-check 192.168.1.10 443 --authorized --execute
python main.py scan 192.168.1.10 --authorized --execute --format html
python main.py analyze examples/sample_scan.xml
```

DNS uses the operating system resolver and supports forward A/AAAA lookup or reverse PTR lookup. TCP connectivity checks connect to exactly one permitted IP and port with a short timeout; they do not retrieve banners or scan adjacent ports.

Profiles: `discover` performs host discovery; `scan` performs a conservative TCP top-100 service review. Arbitrary flags and scripts are not accepted. Reports are local and should be treated as sensitive.
