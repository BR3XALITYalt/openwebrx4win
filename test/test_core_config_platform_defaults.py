import os
import tempfile
import unittest
from pathlib import Path

from owrx.config.core import CoreConfig


class CoreConfigPlatformDefaultsTest(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows defaults are only active on Windows")
    def testWindowsPathsUseWindowsLocations(self):
        local_app_data = os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local")
        data_root = Path(local_app_data) / "OpenWebRX"

        self.assertEqual(
            Path(CoreConfig.defaultSearchLocations[1]),
            data_root / "openwebrx.conf",
        )
        self.assertEqual(
            Path(CoreConfig.defaults["core"]["data_directory"]),
            data_root / "data",
        )
        self.assertEqual(
            Path(CoreConfig.defaults["core"]["temporary_directory"]),
            Path(tempfile.gettempdir()),
        )
        self.assertEqual(
            Path(CoreConfig.defaults["aprs"]["symbols_path"]),
            data_root / "aprs-symbols" / "png",
        )

    @unittest.skipUnless(os.name != "nt", "Non-Windows defaults are not active on Windows")
    def testNonWindowsPathsRemainUnchanged(self):
        self.assertEqual(
            CoreConfig.defaultSearchLocations,
            ["./openwebrx.conf", "/etc/openwebrx/openwebrx.conf"],
        )
        self.assertEqual(
            CoreConfig.defaults["core"]["data_directory"],
            "/var/lib/openwebrx",
        )
        self.assertEqual(
            CoreConfig.defaults["core"]["temporary_directory"],
            "/tmp",
        )
        self.assertEqual(
            CoreConfig.defaults["aprs"]["symbols_path"],
            "/usr/share/aprs-symbols/png",
        )


if __name__ == "__main__":
    unittest.main()
