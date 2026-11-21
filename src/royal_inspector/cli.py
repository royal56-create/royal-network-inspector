"""Command-line interface with fail-closed active-operation gates."""
import argparse
import json
import sys
from pathlib import Path
from .analyzer import analyze
from .diagnostics import dns_lookup, tcp_connect_check
from .history import record_history
from .reports import write_report
from .scanner import build_command, nmap_version, parse_nmap_xml, run_scan
from .validation import subnet_details, validate_target


def parser():
    root = argparse.ArgumentParser(prog="royal-inspector", description="Authorized private-lab network inspection toolkit.")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("scan", "discover"):
        item = commands.add_parser(name, help="Preview or run a bounded Nmap operation.")
        item.add_argument("target", help="Private/loopback/link-local IP or CIDR (maximum 256 addresses).")
        item.add_argument("--authorized", action="store_true", help="Confirm you own the target or have explicit permission.")
        item.add_argument("--execute", action="store_true", help="Actually run Nmap; without this, only a dry-run preview is shown.")
        item.add_argument("--dry-run", action="store_true", help="Preview only (the default).")
        item.add_argument("--format", choices=("json", "csv", "html"), default="json")
        item.add_argument("--output-dir", default="reports")
    check = commands.add_parser("validate", help="Validate an IP address or CIDR.")
    check.add_argument("target")
    subnet = commands.add_parser("subnet", help="Calculate details for a subnet up to 256 addresses.")
    subnet.add_argument("cidr")
    commands.add_parser("nmap-check", help="Check whether Nmap is installed.")
    dns = commands.add_parser("dns", help="Resolve a hostname or perform reverse DNS for an IP.")
    dns.add_argument("name")
    connect = commands.add_parser("connect-check", help="Check one TCP port on an authorized private lab host.")
    connect.add_argument("target")
    connect.add_argument("port", type=int)
    connect.add_argument("--authorized", action="store_true", help="Confirm you own the target or have explicit permission.")
    connect.add_argument("--execute", action="store_true", help="Perform the TCP connection test; default is preview only.")
    offline = commands.add_parser("analyze", help="Analyze an existing Nmap XML file without scanning.")
    offline.add_argument("xml_file")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "validate":
            parsed = validate_target(args.target)
            print(json.dumps({"valid": True, "target": str(parsed), "private": parsed.is_private}, indent=2))
            return 0
        if args.command == "subnet":
            print(json.dumps(subnet_details(args.cidr), indent=2))
            return 0
        if args.command == "nmap-check":
            print(json.dumps(nmap_version(), indent=2))
            return 0
        if args.command == "dns":
            print(json.dumps(dns_lookup(args.name), indent=2))
            return 0
        if args.command == "connect-check":
            validate_target(args.target)
            if not 1 <= args.port <= 65535:
                raise ValueError("Port must be between 1 and 65535.")
            if not args.execute:
                print("DRY RUN — no connection was attempted.")
                print(f"Planned TCP connectivity check: {args.target}:{args.port}")
                print("To proceed, confirm permission and add both --authorized and --execute.")
                return 0
            if not args.authorized:
                print("Blocked: --authorized is required before execution.", file=sys.stderr)
                return 2
            print(json.dumps(tcp_connect_check(args.target, args.port), indent=2))
            return 0
        if args.command == "analyze":
            result = parse_nmap_xml(Path(args.xml_file).read_text(encoding="utf-8"))
            print(json.dumps(analyze(result), indent=2))
            return 0
        mode = "discover" if args.command == "discover" else "scan"
        validate_target(args.target)
        command = build_command(args.target, mode)
        if args.dry_run or not args.execute:
            print("DRY RUN — no network activity was started.")
            print("Planned command:", " ".join(command))
            print("To proceed, confirm permission and add both --authorized and --execute.")
            return 0
        if not args.authorized:
            print("Blocked: --authorized is required before execution.", file=sys.stderr)
            return 2
        outcome = run_scan(args.target, mode)
        result = outcome["result"]
        summary = analyze(result)
        report_path = write_report(result, summary, args.format, args.output_dir)
        record_history(args.target, mode, summary, str(Path(args.output_dir) / "history.json"))
        print(json.dumps({"summary": summary, "report": report_path}, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
