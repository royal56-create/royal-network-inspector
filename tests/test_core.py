import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from royal_inspector.validation import validate_target, subnet_details
from royal_inspector.scanner import build_command, parse_nmap_xml
from royal_inspector.analyzer import analyze

SAMPLE = """<?xml version="1.0"?><nmaprun><host><status state="up"/><address addr="192.168.56.10" addrtype="ipv4"/><hostnames><hostname name="lab-host"/></hostnames><ports><port protocol="tcp" portid="22"><state state="open"/><service name="ssh" product="OpenSSH" version="9.0"/></port><port protocol="tcp" portid="80"><state state="closed"/></port></ports></host></nmaprun>"""

class ValidationTests(unittest.TestCase):
    def test_private_host(self):
        self.assertEqual(str(validate_target("192.168.1.5")), "192.168.1.5")
    def test_public_host_blocked(self):
        with self.assertRaises(ValueError):
            validate_target("8.8.8.8")
    def test_large_range_blocked(self):
        with self.assertRaises(ValueError):
            validate_target("10.0.0.0/16")
    def test_subnet(self):
        self.assertEqual(subnet_details("192.168.1.0/24")["usable_hosts"], 254)

class ParserTests(unittest.TestCase):
    def test_xml_and_analysis(self):
        parsed = parse_nmap_xml(SAMPLE)
        self.assertEqual(parsed["host_count"], 1)
        summary = analyze(parsed)
        self.assertEqual(summary["open_port_count"], 1)
        self.assertEqual(summary["open_ports"][0]["port"], 22)
    def test_fixed_command_profile(self):
        command = build_command("192.168.1.10", "scan")
        self.assertIn("--top-ports", command)
        self.assertIn("100", command)
        self.assertNotIn("-A", command)
    def test_discovery_outputs_xml(self):
        command = build_command("192.168.1.10", "discover")
        self.assertIn("-oX", command)

if __name__ == "__main__":
    unittest.main()
