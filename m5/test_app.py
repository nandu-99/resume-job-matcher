"""Interface behaviour checks using Streamlit's application test runner."""

from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).with_name("app.py")


class StreamlitInterfaceTests(unittest.TestCase):
    def make_app(self, result=None):
        matcher = Mock()
        matcher.predict_match.return_value = result or {
            "label": "Potential Fit", "truncated": False,
            "input_tokens": 12, "original_tokens": 12,
        }
        patcher = patch("m5.service.load_matcher", return_value=matcher)
        patcher.start()
        self.addCleanup(patcher.stop)
        app = AppTest.from_file(str(APP_PATH), default_timeout=60).run()
        self.assertEqual(len(app.exception), 0)
        return app, matcher

    def fill_inputs(self, app):
        app.text_area(key="resume_text").input("Python developer").run()
        app.text_area(key="job_text").input("Python and SQL").run()

    def test_prediction_and_clear(self):
        app, matcher = self.make_app()
        self.assertTrue(app.button(key="analyse_match").disabled)
        self.fill_inputs(app)
        self.assertFalse(app.button(key="analyse_match").disabled)
        app.button(key="analyse_match").click().run()
        self.assertEqual(len(app.exception), 0)
        matcher.predict_match.assert_called_once_with("Python developer", "Python and SQL")
        self.assertIn("Potential Fit", [item.value for item in app.subheader])

        app.button(key="clear_inputs").click().run()
        self.assertEqual(app.text_area(key="resume_text").value, "")
        self.assertEqual(app.text_area(key="job_text").value, "")
        self.assertIsNone(app.session_state["match_result"])
        self.assertTrue(app.button(key="analyse_match").disabled)

    def test_edit_invalidates_previous_result(self):
        app, _ = self.make_app()
        self.fill_inputs(app)
        app.button(key="analyse_match").click().run()
        self.assertIsNotNone(app.session_state["match_result"])
        app.text_area(key="resume_text").input("Updated resume").run()
        self.assertIsNone(app.session_state["match_result"])
        self.assertIn("Your result will appear here", [item.value for item in app.subheader])

    def test_truncation_and_example(self):
        app, _ = self.make_app({
            "label": "No Fit", "truncated": True,
            "input_tokens": 512, "original_tokens": 1200,
        })
        app.button(key="use_example").click().run()
        self.assertTrue(app.text_area(key="resume_text").value)
        self.assertTrue(app.text_area(key="job_text").value)
        app.button(key="analyse_match").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("No Fit", [item.value for item in app.subheader])
        self.assertTrue(any("Long input was shortened" in item.value for item in app.markdown))
        self.assertIsNone(app.session_state["match_error"])

    def test_missing_model_hides_internal_details(self):
        app, _ = self.make_app()
        import m5.service
        m5.service.load_matcher.side_effect = FileNotFoundError("/private/model/path")
        self.fill_inputs(app)
        app.button(key="analyse_match").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.error), 1)
        self.assertNotIn("/private/", app.error[0].value)
        self.assertIn("unavailable", app.error[0].value)
        self.assertEqual(app.text_area(key="resume_text").value, "Python developer")

    def test_oversized_resume_does_not_load_model(self):
        app, matcher = self.make_app()
        import m5.service
        app.text_area(key="resume_text").input("a" * 50_001).run()
        app.text_area(key="job_text").input("Python and SQL").run()
        app.button(key="analyse_match").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("50,000", app.error[0].value)
        m5.service.load_matcher.assert_not_called()
        matcher.predict_match.assert_not_called()
        self.assertEqual(len(app.text_area(key="resume_text").value), 50_001)

    def test_retry_after_model_load_failure(self):
        app, matcher = self.make_app()
        import m5.service
        m5.service.load_matcher.side_effect = [ValueError("private checkpoint detail"), matcher]
        self.fill_inputs(app)
        app.button(key="analyse_match").click().run()
        self.assertIn("unavailable", app.error[0].value)
        self.assertIsNone(app.session_state["pending_action"])
        self.assertFalse(app.button(key="analyse_match").disabled)
        self.assertTrue(app.session_state["match_error_reference"])
        self.assertIsNone(app.session_state["match_result"])
        app.button(key="analyse_match").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.error), 0)
        self.assertIsNone(app.session_state["match_error_reference"])
        self.assertIn("Potential Fit", [item.value for item in app.subheader])

    def test_prediction_failure_clears_old_result(self):
        app, matcher = self.make_app()
        self.fill_inputs(app)
        app.button(key="analyse_match").click().run()
        self.assertIsNotNone(app.session_state["match_result"])
        matcher.predict_match.side_effect = RuntimeError("private document text")
        app.button(key="analyse_match").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIsNone(app.session_state["match_result"])
        self.assertNotIn("private document", app.error[0].value)
        self.assertTrue(app.session_state["match_error_reference"])


if __name__ == "__main__":
    unittest.main()
