import unittest
from unittest.mock import Mock, patch

from owrx.feature import FeatureDetector


class FeatureDetectorCommandTest(unittest.TestCase):
    def setUp(self):
        self.detector = FeatureDetector()

    def run_command(self, exit_code, expected_result=None):
        process = Mock()
        process.wait.return_value = exit_code

        with patch("owrx.feature.CoreConfig") as core_config:
            core_config.return_value.get_temporary_directory.return_value = "."
            with patch("owrx.feature.subprocess.Popen", return_value=process):
                return self.detector.command_is_runnable(
                    "example-command --help",
                    expected_result=expected_result,
                )

    def testLaunchedCommandIsRunnableWhenHelpReturnsNonzero(self):
        self.assertTrue(self.run_command(32512))

    def testExpectedExitCodeIsCheckedWhenProvided(self):
        self.assertTrue(self.run_command(2, expected_result=2))
        self.assertFalse(self.run_command(2, expected_result=0))


if __name__ == "__main__":
    unittest.main()
