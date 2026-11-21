"""Strict target validation for the authorized private-lab scope."""
from ipaddress import ip_address, ip_network

MAX_ADDRESSES = 256


def validate_target(target: str):
    if not isinstance(target, str) or not target.strip():
        raise ValueError("Target cannot be empty.")
    value = target.strip()
    try:
        parsed = ip_network(value, strict=False) if "/" in value else ip_address(value)
    except ValueError as exc:
        raise ValueError(f"Invalid IP address or CIDR: {value}") from exc
    count = parsed.num_addresses if "/" in value else 1
    if count > MAX_ADDRESSES:
        raise ValueError(f"Target range too large ({count}); maximum is {MAX_ADDRESSES}.")
    if not (parsed.is_private or parsed.is_loopback or parsed.is_link_local):
        raise ValueError("Only private, loopback, or link-local targets are accepted. Public targets are blocked.")
    return parsed


def subnet_details(cidr: str) -> dict:
    network = ip_network(cidr, strict=False)
    if network.num_addresses > MAX_ADDRESSES:
        raise ValueError(f"Subnet exceeds the {MAX_ADDRESSES}-address limit.")
    hosts = list(network.hosts())
    return {
        "network": str(network), "version": network.version, "netmask": str(network.netmask),
        "broadcast": str(network.broadcast_address) if network.version == 4 else None,
        "total_addresses": network.num_addresses, "usable_hosts": len(hosts),
        "first_host": str(hosts[0]) if hosts else None, "last_host": str(hosts[-1]) if hosts else None,
    }
