"""Provisioning checks without network access or real credentials."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from m5.deployment import DOWNLOAD_FILES, provision_model


class DeploymentTests(unittest.TestCase):
    def test_complete_local_model_never_downloads(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in DOWNLOAD_FILES:
                (Path(directory) / name).touch()
            with patch("m5.deployment.snapshot_download") as download:
                provision_model(directory)
                download.assert_not_called()

    def test_missing_local_model_without_remote_stays_local(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            with patch("m5.deployment.snapshot_download") as download:
                provision_model(directory)
                download.assert_not_called()

    def test_remote_requires_immutable_revision(self):
        for revision in ("", "main", "abc123"):
            with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
                "RESUME_MATCHER_HF_REPO": "team/model", "RESUME_MATCHER_HF_REVISION": revision,
            }, clear=True), patch("m5.deployment.snapshot_download") as download:
                with self.assertRaises(ValueError):
                    provision_model(directory)
                download.assert_not_called()

    def test_download_is_pinned_and_restricted_to_inference_files(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
            "RESUME_MATCHER_HF_REPO": "team/model", "RESUME_MATCHER_HF_REVISION": "a" * 40,
            "HF_TOKEN": "test-read-token",
        }, clear=True), patch("m5.deployment.snapshot_download") as download:
            provision_model(directory)
            download.assert_called_once_with(
                repo_id="team/model", revision="a" * 40, token="test-read-token",
                allow_patterns=list(DOWNLOAD_FILES), local_dir=Path(directory), max_workers=2,
            )


if __name__ == "__main__":
    unittest.main()
