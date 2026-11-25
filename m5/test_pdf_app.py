"""Verify PDF review, input modes, errors, and clearing in the Streamlit UI."""

import io
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from streamlit.testing.v1 import AppTest

from m5.pdf_input import ExtractedPDF, PDFInputError


APP = Path(__file__).with_name("app.py")


class PDFInterfaceTests(unittest.TestCase):
    def make_app(self):
        matcher = Mock()
        matcher.predict_match.return_value = {
            "label": "Potential Fit", "truncated": False, "input_tokens": 12, "original_tokens": 12,
        }
        patcher = patch("m5.service.load_matcher", return_value=matcher)
        patcher.start()
        self.addCleanup(patcher.stop)
        return AppTest.from_file(str(APP)).run(timeout=60), matcher

    def test_reviewed_extraction_reaches_existing_service_and_clear_resets_upload_mode(self):
        app, matcher = self.make_app()
        with patch("m5.app.st.file_uploader", return_value=io.BytesIO(b"synthetic")), patch(
            "m5.pdf_input.extract_pdf", return_value=ExtractedPDF("Python developer", 1, (1,), ()),
        ) as reader:
            app.radio(key="resume_source").set_value("Upload PDF").run()
            self.assertTrue(app.button(key="analyse_match").disabled)
            app.button(key="resume_read_pdf").click().run()
            reader.assert_called_once_with(b"synthetic", force_ocr=False)
            self.assertEqual(app.text_area(key="resume_text").value, "Python developer")
            app.text_area(key="resume_text").input("Reviewed Python developer").run()
            app.text_area(key="job_text").input("Python and SQL").run()
            app.button(key="analyse_match").click().run()
            self.assertFalse(app.exception)
            matcher.predict_match.assert_called_once_with("Reviewed Python developer", "Python and SQL")
            app.button(key="clear_inputs").click().run()
            self.assertEqual(app.radio(key="resume_source").value, "Paste text")
            self.assertEqual(app.text_area(key="resume_text").value, "")
            self.assertIsNone(app.session_state["resume_pdf_report"])

    def test_extraction_failure_prevents_prediction_and_source_change_clears_old_result(self):
        app, matcher = self.make_app()
        app.button(key="use_example").click().run()
        app.button(key="analyse_match").click().run()
        self.assertIsNotNone(app.session_state["match_result"])
        with patch("m5.app.st.file_uploader", return_value=io.BytesIO(b"synthetic")), patch(
            "m5.pdf_input.extract_pdf", side_effect=PDFInputError("The PDF is damaged."),
        ):
            app.radio(key="job_source").set_value("Upload PDF").run()
            self.assertIsNone(app.session_state["match_result"])
            app.button(key="job_read_pdf").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(app.button(key="analyse_match").disabled)
            self.assertIn("The PDF is damaged.", [error.value for error in app.error])
            self.assertEqual(matcher.predict_match.call_count, 1)

    def test_force_ocr_change_invalidates_extraction(self):
        app, _ = self.make_app()
        with patch("m5.app.st.file_uploader", return_value=io.BytesIO(b"synthetic")), patch(
            "m5.pdf_input.extract_pdf", return_value=ExtractedPDF("Python developer", 1, (1,), ()),
        ) as reader:
            app.radio(key="resume_source").set_value("Upload PDF").run()
            app.button(key="resume_read_pdf").click().run()
            app.checkbox[0].check().run()
            self.assertIsNone(app.session_state["resume_pdf_report"])
            self.assertEqual(app.session_state["resume_text"], "")
            self.assertTrue(app.text_area(key="resume_text").disabled)
            app.button(key="resume_read_pdf").click().run()
            self.assertTrue(reader.call_args.kwargs["force_ocr"])


if __name__ == "__main__":
    unittest.main()
