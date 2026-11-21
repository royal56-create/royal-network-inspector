# User Guide

## Safety model
The default is preview-only. A real operation requires both `--authorized` and `--execute`. Targets must be private, loopback, or link-local and no larger than 256 addresses. Obtain permission from the owner even for private networks.

## Examples
```bash
python main.py validate 192.168.1.10
python main.py subnet 192.168.1.0/24
python main.py scan 192.168.1.10 --dry-run
python main.py discover 192.168.1.0/24 --dry-run
python main.py scan 192.168.1.10 --authorized --execute --format html
python main.py analyze examples/sample_scan.xml
```

Profiles: `discover` performs host discovery; `scan` performs a conservative TCP top-100 service review. Arbitrary flags and scripts are not accepted. Reports are local and should be treated as sensitive.
