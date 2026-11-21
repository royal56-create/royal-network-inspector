# Troubleshooting

- **Nmap not found:** install Nmap and ensure it is on PATH; run `python main.py nmap-check`.
- **Target rejected:** only private, loopback, or link-local targets are accepted; CIDR ranges are capped at 256 addresses.
- **Permission denied:** obtain authorization from the network owner. Do not bypass checks.
- **No hosts found:** firewalls may block discovery probes; no response does not prove a host is offline.
- **Service details missing:** detection is probabilistic and depends on responses.
- **Timeout:** the scanner stops after its bounded timeout; do not increase scan intensity to force a response.
