# Installation

Requirements: Python 3.10+; Nmap for actual scans (not needed for dry-run, offline XML analysis, or tests).

Create an environment and install the package:
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Install Nmap from its official distribution or your operating system's trusted package manager. Verify with `nmap --version` and `python main.py nmap-check`.

Run tests:
```bash
python -m unittest discover -s tests -v
python main.py --help
```
