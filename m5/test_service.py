"""Request-boundary, recovery, and log-privacy regression checks."""

import json
import unittest
from unittest.mock import Mock, patch

from m5.inference import predict_match
from m5.service import (
    LOGGER, ModelUnavailableError, PredictionError, analyse_match,
)
from m5.validation import InputValidationError, MAX_INPUT_CHARACTERS, validate_inputs


class ValidationTests(unittest.TestCase):
    def test_invalid_input_never_loads_model(self):
        invalid_pairs = [
            (None, "Python"), ("Python", []), ("", "Python"),
            ("Python", " \n\t"), ("!?!", "Python"),
            ("Python\x00private", "Python"),
            ("a" * (MAX_INPUT_CHARACTERS + 1), "Python"),
            ("Python", "a" * (MAX_INPUT_CHARACTERS + 1)),
            ("[ ](https://example.com)", "Python"),
        ]
        with patch("m5.service.load_matcher") as loader, self.assertLogs(LOGGER) as logs:
            for index, pair in enumerate(invalid_pairs):
                with self.subTest(case=index), self.assertRaises(InputValidationError):
                    analyse_match(*pair)
            loader.assert_not_called()
        self.assertEqual(len(logs.records), len(invalid_pairs))
        self.assertTrue(all(json.loads(r.getMessage())["event"] == "validation_failed"
                            for r in logs.records))

    def test_exact_character_limit_and_technical_text_are_accepted(self):
        validate_inputs("a" * MAX_INPUT_CHARACTERS, "Python and SQL")
        validate_inputs("C++, C#, .NET\nPython\tSQL", "Developer\r\nrole")

    def test_direct_api_rejects_before_cached_loading(self):
        with patch("m5.inference._cached_matcher") as loader:
            with self.assertRaises(InputValidationError):
                predict_match("a" * (MAX_INPUT_CHARACTERS + 1), "Python")
            with self.assertRaises(InputValidationError):
                predict_match("[ ](https://example.com)", "Python")
            loader.assert_not_called()


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.matcher = Mock()
        self.result = {
            "label": "Potential Fit", "truncated": False,
            "input_tokens": 12, "original_tokens": 12,
        }
        self.matcher.predict_match.return_value = self.result
        loader_patch = patch("m5.service.load_matcher", return_value=self.matcher)
        self.loader = loader_patch.start()
        self.addCleanup(loader_patch.stop)
        reset_patch = patch("m5.service.clear_matcher_cache")
        self.reset = reset_patch.start()
        self.addCleanup(reset_patch.stop)

    def test_model_load_errors_are_safe_and_can_retry(self):
        for error in [FileNotFoundError("PRIVATE_PATH"),
                      ValueError("PRIVATE_CHECKPOINT"), RuntimeError("PRIVATE_RUNTIME")]:
            with self.subTest(error=type(error).__name__):
                self.reset.reset_mock()
                self.loader.side_effect = [error, self.matcher]
                with self.assertLogs(LOGGER) as logs:
                    with self.assertRaises(ModelUnavailableError) as caught:
                        analyse_match("Python developer", "Python and SQL")
                    self.assertEqual(analyse_match("Python developer", "Python and SQL"), self.result)
                self.assertNotIn("PRIVATE", str(caught.exception))
                self.reset.assert_called_once_with()
                records = [json.loads(r.getMessage()) for r in logs.records]
                self.assertNotIn("PRIVATE", " ".join(r.getMessage() for r in logs.records))
                self.assertTrue(all(r.exc_info is None for r in logs.records))
                self.assertEqual([r["event"] for r in records],
                                 ["model_load_failed", "prediction_completed"])
                self.assertEqual(caught.exception.request_id, records[0]["request_id"])

    def test_prediction_failure_resets_cache_and_can_retry(self):
        self.matcher.predict_match.side_effect = [RuntimeError("PRIVATE_DOCUMENT"), self.result]
        with self.assertLogs(LOGGER) as logs:
            with self.assertRaises(PredictionError) as caught:
                analyse_match("Python developer", "Python and SQL")
            self.assertEqual(analyse_match("Python developer", "Python and SQL"), self.result)
        self.assertNotIn("PRIVATE_DOCUMENT", str(caught.exception))
        self.assertNotIn("PRIVATE_DOCUMENT", " ".join(r.getMessage() for r in logs.records))
        self.assertTrue(all(r.exc_info is None for r in logs.records))
        self.reset.assert_called_once_with()
        self.assertEqual([json.loads(r.getMessage())["event"] for r in logs.records],
                         ["prediction_failed", "prediction_completed"])

    def test_invalid_model_responses_are_not_displayable_predictions(self):
        invalid_results = [None, {}, {**self.result, "label": "Unknown"},
                           {**self.result, "input_tokens": True},
                           {**self.result, "original_tokens": 1200},
                           {**self.result, "truncated": "false"}]
        with self.assertLogs(LOGGER):
            for index, result in enumerate(invalid_results):
                with self.subTest(case=index):
                    self.matcher.predict_match.return_value = result
                    with self.assertRaises(PredictionError):
                        analyse_match("Python developer", "Python and SQL")
        self.assertEqual(self.reset.call_count, len(invalid_results))

    def test_logs_contain_only_operational_metadata(self):
        resume, job = "PRIVATE_RESUME_CONTENT", "PRIVATE_JOB_CONTENT"
        with self.assertLogs(LOGGER) as logs:
            result = analyse_match(resume, job)
        self.assertEqual(result, self.result)
        self.matcher.predict_match.assert_called_once_with(resume, job)
        self.reset.assert_not_called()
        self.assertEqual(len(logs.records), 1)
        record = json.loads(logs.records[0].getMessage())
        self.assertEqual(set(record), {
            "event", "request_id", "duration_ms", "resume_chars", "job_chars", "truncated"
        })
        self.assertEqual(record["resume_chars"], len(resume))
        self.assertEqual(record["job_chars"], len(job))
        self.assertGreaterEqual(record["duration_ms"], 0)
        self.assertRegex(record["request_id"], r"^[a-f0-9]{12}$")
        self.assertNotIn(resume, logs.records[0].getMessage())
        self.assertNotIn(job, logs.records[0].getMessage())
        self.assertNotIn(self.result["label"], logs.records[0].getMessage())
        self.assertIsNone(logs.records[0].exc_info)


if __name__ == "__main__":
    unittest.main()
