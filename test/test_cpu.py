import os
import time
import unittest
from unittest.mock import mock_open, patch

from owrx.cpu import CpuUsageThread


class CpuUsageTest(unittest.TestCase):
    def make_thread(self):
        thread = CpuUsageThread.__new__(CpuUsageThread)
        thread.last_worktime = 0
        thread.last_idletime = 0
        return thread

    @unittest.skipUnless(os.name == "nt", "Win32 CPU accounting is only used on Windows")
    def testWindowsReadsSystemTimes(self):
        thread = self.make_thread()

        first = thread.get_cpu_usage()
        time.sleep(0.05)
        second = thread.get_cpu_usage()

        self.assertGreaterEqual(first, 0)
        self.assertLessEqual(first, 1)
        self.assertGreaterEqual(second, 0)
        self.assertLessEqual(second, 1)

    @unittest.skipIf(os.name == "nt", "Linux CPU accounting is not used on Windows")
    def testLinuxReadsProcStat(self):
        thread = self.make_thread()
        with patch(
            "builtins.open",
            mock_open(read_data="cpu  100 10 20 200 30 0 0 0\n"),
        ):
            usage = thread.get_cpu_usage()

        self.assertAlmostEqual(usage, 130 / 330)

    @unittest.skipIf(os.name == "nt", "Linux CPU accounting is not used on Windows")
    def testLinuxReturnsZeroWhenProcStatIsUnavailable(self):
        thread = self.make_thread()
        with patch("builtins.open", side_effect=OSError("missing")):
            self.assertEqual(thread.get_cpu_usage(), 0)


if __name__ == "__main__":
    unittest.main()
