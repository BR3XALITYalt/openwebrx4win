import unittest
from unittest.mock import Mock, patch

from owrx.process import get_process_start_options, stop_process


class ProcessStartOptionsTest(unittest.TestCase):
    def testWindowsUsesASeparateProcessGroup(self):
        with patch("owrx.process.subprocess.CREATE_NEW_PROCESS_GROUP", 0x0200, create=True):
            self.assertEqual(
                get_process_start_options(is_windows=True),
                {"creationflags": 0x0200},
            )

    def testNonWindowsUsesANewSession(self):
        self.assertEqual(
            get_process_start_options(is_windows=False),
            {"start_new_session": True},
        )


class StopProcessTest(unittest.TestCase):
    def testWindowsSendsBreakEvent(self):
        process = Mock()
        monitor = Mock()
        monitor.is_alive.return_value = False

        with patch("owrx.process.signal.CTRL_BREAK_EVENT", 1, create=True):
            forced = stop_process(process, monitor, is_windows=True)

        self.assertFalse(forced)
        process.send_signal.assert_called_once_with(1)
        process.terminate.assert_not_called()
        process.kill.assert_not_called()
        monitor.join.assert_called_once_with(10)

    def testWindowsFallsBackToTerminateWhenBreakEventFails(self):
        process = Mock()
        process.send_signal.side_effect = OSError("no console")
        monitor = Mock()
        monitor.is_alive.return_value = False

        with patch("owrx.process.signal.CTRL_BREAK_EVENT", 1, create=True):
            forced = stop_process(process, monitor, is_windows=True)

        self.assertFalse(forced)
        process.send_signal.assert_called_once_with(1)
        process.terminate.assert_called_once_with()

    def testWindowsKillsProcessAfterTimeout(self):
        process = Mock()
        monitor = Mock()
        monitor.is_alive.return_value = True

        forced = stop_process(process, monitor, is_windows=True)

        self.assertTrue(forced)
        process.kill.assert_called_once_with()

    def testNonWindowsStopsProcessGroup(self):
        process = Mock(pid=1234)
        monitor = Mock()
        monitor.is_alive.return_value = False

        with patch("owrx.process.os.getpgid", return_value=1234, create=True), patch(
            "owrx.process.os.killpg", create=True
        ) as killpg, patch("owrx.process.signal.SIGKILL", 9, create=True):
            forced = stop_process(process, monitor, is_windows=False)

        self.assertFalse(forced)
        killpg.assert_called_once()
        self.assertEqual(killpg.call_args.args[0], 1234)

    def testNonWindowsForceKillsProcessGroupAfterTimeout(self):
        process = Mock(pid=1234)
        monitor = Mock()
        monitor.is_alive.return_value = True

        with patch("owrx.process.os.getpgid", return_value=1234, create=True), patch(
            "owrx.process.os.killpg", create=True
        ) as killpg, patch("owrx.process.signal.SIGKILL", 9, create=True):
            forced = stop_process(process, monitor, is_windows=False)

        self.assertTrue(forced)
        self.assertEqual(killpg.call_count, 2)


if __name__ == "__main__":
    unittest.main()
