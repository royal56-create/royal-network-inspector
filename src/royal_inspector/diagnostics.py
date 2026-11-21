"""Small, bounded diagnostics; no scanning or service-banner collection."""
import socket
from ipaddress import ip_address
from .validation import validate_target


def dns_lookup(name: str) -> dict:
    value = name.strip()
    if not value:
        raise ValueError("A hostname or IP address is required.")
    try:
        address = ip_address(value)
    except ValueError:
        # Resolve a hostname using the operating system's configured resolver.
        try:
            records = socket.getaddrinfo(value, None, type=socket.SOCK_STREAM)
        except socket.gaierror as exc:
            raise RuntimeError(f"DNS lookup failed: {exc}") from exc
        addresses = sorted({item[4][0] for item in records})
        return {"query": value, "record_type": "A/AAAA", "addresses": addresses}
    try:
        hostname, aliases, _ = socket.gethostbyaddr(str(address))
        return {"query": value, "record_type": "PTR", "hostname": hostname, "aliases": aliases}
    except (socket.herror, socket.gaierror):
        return {"query": value, "record_type": "PTR", "hostname": None, "aliases": []}


def tcp_connect_check(target: str, port: int, timeout: float = 2.0) -> dict:
    address = validate_target(target)
    if "/" in target:
        raise ValueError("TCP connectivity check accepts one IP address, not a CIDR range.")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    try:
        with socket.create_connection((str(address), port), timeout=timeout):
            return {"target": str(address), "port": port, "reachable": True, "result": "connected"}
    except (OSError, TimeoutError) as exc:
        return {"target": str(address), "port": port, "reachable": False, "result": type(exc).__name__}
