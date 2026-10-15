"""Offline retirement checks; never publish an edition."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ingest', ROOT / 'reading/ingest.py')
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)


class RetirementTests(unittest.TestCase):
    def test_write_and_network_modes_fail_before_side_effects(self):
        for args in [[], ['https://x.com/example/status/1'], ['--dry-run', 'https://x.com/example/status/1'],
                     ['--no-push', '--thread-file', 'unused'], ['--dry-run', '--thread-file', 'unused']]:
            with self.subTest(args=args), patch.object(sys, 'argv', ['ingest.py', *args]), \
                 patch.object(ingest, 'fetch_thread', side_effect=AssertionError('network')), \
                 patch.object(ingest, 'make_summary', side_effect=AssertionError('provider')), \
                 patch.object(ingest, 'push_changes', side_effect=AssertionError('publish')):
                with self.assertRaises(SystemExit) as result:
                    ingest.main()
                self.assertEqual(result.exception.code, 2)

    def test_offline_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'thread.txt'
            raw.write_text('@example (Example):\nSynthetic article title\n\nSynthetic body.\n')
            with patch.object(sys, 'argv', ['ingest.py', '--dry-run', '--thread-file', str(raw), '--no-summary']), \
                 patch.object(ingest, 'update_json', side_effect=AssertionError('write')), \
                 patch.object(ingest, 'bump_sw', side_effect=AssertionError('write')):
                ingest.main()
            self.assertEqual(list(Path(directory).iterdir()), [raw])


if __name__ == '__main__':
    unittest.main()
