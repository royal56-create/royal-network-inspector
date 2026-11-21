import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from royal_inspector.cli import main

class CliTests(unittest.TestCase):
    def test_default_is_dry_run(self):
        with patch("builtins.print") as output:
            self.assertEqual(main(["scan", "192.168.1.10"]), 0)
        self.assertTrue(any("DRY RUN" in str(call) for call in output.call_args_list))
    def test_execute_requires_authorization(self):
        with patch("builtins.print"):
            self.assertEqual(main(["scan", "192.168.1.10", "--execute"]), 2)

if __name__ == "__main__":
    unittest.main()
