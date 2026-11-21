"""Summaries and cautious informational risk hints."""
def analyze(result: dict) -> dict:
    hosts = result.get("hosts", [])
    open_ports = []
    for host in hosts:
        address = next((a["address"] for a in host.get("addresses", []) if a.get("type") in ("ipv4", "ipv6")), "unknown")
        for port in host.get("ports", []):
            if port.get("state") == "open":
                open_ports.append({"host": address, **port})
    hints = []
    for item in open_ports:
        number = item.get("port")
        if number in (21, 23, 445, 3389):
            hints.append({"host": item["host"], "port": number, "level": "review",
                          "reason": "Commonly sensitive service; verify necessity and access controls."})
        elif number in (80, 8080):
            hints.append({"host": item["host"], "port": number, "level": "info",
                          "reason": "Review web-service configuration and transport security."})
    return {"host_count": len(hosts), "open_port_count": len(open_ports), "open_ports": open_ports,
            "review_hints": hints,
            "note": "Heuristic learning hints only; not a vulnerability scanner or security certification."}
