# Contributing

- Keep changes defensive, educational, and limited to explicitly authorized lab use.
- Do not add exploit modules, brute force, stealth/evasion, DoS, credential harvesting, or public-target scanning.
- Add tests for parsing, validation, and reporting changes. Tests must use synthetic data and never perform network scans.
- Run `python -m unittest discover -s tests -v` and `python -m compileall -q src main.py`.
- Update README, CHANGELOG, and PROJECT_STATUS when behavior changes.

Contributions are provided under the repository's MIT license.
