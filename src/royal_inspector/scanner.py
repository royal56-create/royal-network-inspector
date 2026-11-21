"""Conservative Nmap wrapper. No shell, arbitrary flags, or public targets."""
import shutil
import subprocess
import xml.etree.ElementTree as ET
from .validation import validate_target


def nmap_version():
    executable = shutil.which("nmap")
    if not executable:
        return {"available": False, "path": None, "version": None}
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10, check=False)
    lines = (result.stdout or result.stderr).splitlines()
    return {"available": result.returncode == 0, "path": executable, "version": lines[0] if lines else "Unknown"}


def build_command(target: str, mode: str = "scan") -> list[str]:
    target_text = str(validate_target(target))
    executable = shutil.which("nmap") or "nmap"
    if mode == "discover":
        return [executable, "-sn", "-T2", "--", target_text]
    if mode == "scan":
        return [executable, "-sV", "--version-light", "--top-ports", "100", "-T2", "-oX", "-", "--", target_text]
    raise ValueError("Unsupported scan mode.")


def parse_nmap_xml(source) -> dict:
    root = ET.fromstring(source) if isinstance(source, str) else source
    hosts = []
    for host in root.findall("host"):
        status = host.find("status")
        addresses = [{"type": item.get("addrtype"), "address": item.get("addr")} for item in host.findall("address")]
        names = [item.get("name") for item in host.findall("./hostnames/hostname") if item.get("name")]
        ports = []
        for port in host.findall("./ports/port"):
            state, service = port.find("state"), port.find("service")
            ports.append({
                "protocol": port.get("protocol"), "port": int(port.get("portid", "0")),
                "state": state.get("state") if state is not None else "unknown",
                "service": service.get("name") if service is not None else None,
                "product": service.get("product") if service is not None else None,
                "version": service.get("version") if service is not None else None,
            })
        osmatch = host.find("./os/osmatch")
        hosts.append({
            "status": status.get("state") if status is not None else "unknown",
            "addresses": addresses, "hostnames": names,
            "os_guess": osmatch.get("name") if osmatch is not None else None, "ports": ports,
        })
    return {"hosts": hosts, "host_count": len(hosts)}


def run_scan(target: str, mode: str = "scan", timeout: int = 180) -> dict:
    command = build_command(target, mode)
    executable = shutil.which("nmap")
    if not executable:
        raise RuntimeError("Nmap is not installed or is not available on PATH.")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Nmap exceeded the {timeout}-second timeout and was stopped.") from exc
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "Nmap failed.").strip()[:1200])
    try:
        parsed = parse_nmap_xml(result.stdout)
    except ET.ParseError as exc:
        raise RuntimeError("Nmap output could not be parsed as XML.") from exc
    return {"command": command, "result": parsed}
