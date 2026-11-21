import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from royal_inspector.diagnostics import dns_lookup, tcp_connect_check
from royal_inspector.validation import validate_target

class DiagnosticsTests(unittest.TestCase):
    @patch("royal_inspector.diagnostics.socket.getaddrinfo")
    def test_dns_deduplicates_addresses(self, resolver):
        resolver.return_value = [
            (2, 1, 6, "", ("192.168.1.10", 0)),
            (2, 1, 6, "", ("192.168.1.10", 0)),
        ]
        self.assertEqual(dns_lookup("lab.local")["addresses"], ["192.168.1.10"])

    def test_public_ip_is_blocked(self):
        with self.assertRaises(ValueError):
            validate_target("1.1.1.1")

    def test_unspecified_ip_is_blocked(self):
        with self.assertRaises(ValueError):
            validate_target("0.0.0.0")

    def test_cidr_not_allowed_for_connect_check(self):
        with self.assertRaises(ValueError):
            tcp_connect_check("192.168.1.0/24", 80)

    def test_invalid_port_rejected(self):
        with self.assertRaises(ValueError):
            tcp_connect_check("192.168.1.10", 70000)

if __name__ == "__main__":
    unittest.main()
