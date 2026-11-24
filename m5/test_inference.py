"""Run from the repository root: python -m unittest discover -s m5 -v."""

import csv
import os
from pathlib import Path
import tempfile
import unittest

from m5.inference import (
    LABELS, MODEL_FILES, ResumeJobMatcher, load_matcher, prepare_text,
    resolve_model_dir,
)


class PreparationTests(unittest.TestCase):
    def test_technical_text_and_contact_preparation(self):
        source = (
            "  Skills: C++, C#, .NET\r\n"
            "[Portfolio](https://example.com)\n\n"
            "Contact: person@example.com +1 (212) 555-0199  "
        )
        self.assertEqual(
            prepare_text(source),
            "Skills: C++, C#, .NET\nPortfolio\nContact: email phone",
        )
        self.assertEqual(prepare_text("Ｐｙｔｈｏｎ\tSQL"), "Python SQL")

    def test_rejects_another_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in MODEL_FILES:
                (Path(directory) / name).write_text("not the selected artifact")
            with self.assertRaisesRegex(ValueError, "checkpoint does not match"):
                ResumeJobMatcher(directory)


@unittest.skipUnless(
    (resolve_model_dir() / "model.safetensors").is_file(),
    "Extract the selected model archive to run CPU integration checks.",
)
class CPUInferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matcher = load_matcher(device="cpu")

    def test_result_contract(self):
        result = self.matcher.predict_match("Python developer", "Python and SQL")
        self.assertEqual(next(self.matcher.model.parameters()).device.type, "cpu")
        self.assertFalse(self.matcher.model.training)
        self.assertEqual(
            set(result), {"label", "truncated", "input_tokens", "original_tokens"}
        )
        self.assertIn(result["label"], LABELS)
        self.assertFalse(result["truncated"])
        self.assertEqual(result["input_tokens"], result["original_tokens"])

    def test_truncation_boundary_includes_pair_special_tokens(self):
        at_limit = self.matcher.predict_match("python " * 255, "sql " * 254)
        over_limit = self.matcher.predict_match("python " * 256, "sql " * 254)
        self.assertEqual(at_limit["original_tokens"], 512)
        self.assertFalse(at_limit["truncated"])
        self.assertEqual(over_limit["original_tokens"], 513)
        self.assertTrue(over_limit["truncated"])
        self.assertEqual(over_limit["input_tokens"], 512)

    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            self.matcher.predict_match(None, "Python")
        with self.assertRaises(ValueError):
            self.matcher.predict_match(" \n ", "Python")
        with self.assertRaises(ValueError):
            self.matcher.predict_match("[ ](https://example.com)", "Python")

    @unittest.skipUnless(
        os.environ.get("RESUME_MATCHER_REVIEW_CSV"),
        "Set RESUME_MATCHER_REVIEW_CSV to the private M4 review CSV for parity checks.",
    )
    def test_saved_validation_predictions(self):
        with Path(os.environ["RESUME_MATCHER_REVIEW_CSV"]).open(newline="") as file:
            cases = list(csv.DictReader(file))
        self.assertEqual(len(cases), 30)
        for case in cases:
            with self.subTest(source_row_id=case["source_row_id"]):
                result = self.matcher.predict_match(
                    case["resume_model_text"], case["job_model_text"]
                )
                self.assertEqual(result["label"], case["weighted_prediction"])


if __name__ == "__main__":
    unittest.main()
