# Scan Profiles

| Profile | Fixed behavior | Purpose |
|---|---|---|
| discover | `nmap -sn -oX - -T2` | Host discovery in a permitted lab |
| scan | `nmap -sV --version-light --top-ports 100 -T2 -oX -` | Conservative TCP service review |

Targets are validated before execution. No arbitrary flags, NSE scripts, UDP sweep, OS fingerprinting, stealth options, or aggressive timing are exposed in this release. This is an intentional safety boundary.
