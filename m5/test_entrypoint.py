"""Exercise hosted entry point and the protected measurement view."""

from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


ENTRY = Path(__file__).parents[1] / "streamlit_app.py"


class EntrypointTests(unittest.TestCase):
    def test_normal_app_starts_without_credentials(self):
        app = AppTest.from_file(str(ENTRY)).run(timeout=60)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.text_area), 2)

    def test_measurement_requires_password(self):
        app = AppTest.from_file(str(ENTRY))
        app.secrets["PERFORMANCE_TOKEN"] = "test-password"
        app.query_params["performance"] = "1"
        with patch("m5.benchmark.run_benchmark") as benchmark:
            app.run(timeout=60)
            self.assertFalse(app.exception)
            self.assertEqual(len(app.button), 0)
            app.text_input[0].input("wrong").run()
            benchmark.assert_not_called()
            app.text_input[0].input("test-password").run()
            self.assertEqual(app.button[0].label, "Measure performance")
            benchmark.return_value = {"scope": "synthetic test"}
            app.button[0].click().run()
            benchmark.assert_called_once_with()
            self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
