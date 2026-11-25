# Streamlit deployment

The application is prepared for Streamlit Community Cloud. Publishing and hosted verification are still to be done by the maintainer. The frozen class-weighted checkpoint and white interface are unchanged.

## 1. Store the selected model

Create a **private model repository** on Hugging Face. Upload only these files from the extracted `distilbert_weighted_v1_model.zip`, at the repository root:

```text
config.json
model.safetensors
tokenizer.json
tokenizer_config.json
```

Do not upload resumes, review CSVs, training data, or the entire project. Use the selected trained weights, not `distilbert-base-uncased`. The application checks the weight SHA-256 against `m4/evaluation/model_selection.json` before inference:

```text
004d162ccc9daa4311ff9edeecb1e860a3638a5d0e0c530f5a929df7a40d4b72
```

Open the model repository's commit history after uploading and copy the **full 40-character commit SHA**. This is the new model-hosting repository's commit, not the original pretrained model revision. Create a read-only or fine-grained read token with access to that private model repository.

## 2. Commit the application and deploy

After review, commit and push these changes yourself. In Streamlit Community Cloud:

1. Create an app and select this GitHub repository and the branch containing these changes.
2. Set the entry point to **`streamlit_app.py`** at the repository root.
3. In Advanced settings, select **Python 3.14** if available, matching the local runtime. If unavailable, use 3.13 and verify installation and all checks in that environment before recording deployment as verified.
4. Paste the settings below into the Secrets field, using your actual repository, revision, and token.
5. Deploy and open the app. Use the synthetic example for the first prediction.

```toml
RESUME_MATCHER_HF_REPO = "YOUR_USERNAME/resume-job-matcher-weighted"
RESUME_MATCHER_HF_REVISION = "FULL_40_CHARACTER_MODEL_REPOSITORY_COMMIT_SHA"
HF_TOKEN = "YOUR_READ_ONLY_TOKEN"
PERFORMANCE_TOKEN = "YOUR_LONG_RANDOM_MAINTAINER_PASSWORD"
```

The example file is [.streamlit/secrets.toml.example](../.streamlit/secrets.toml.example). Never commit actual secrets. Root-level Streamlit secrets provide the environment settings consumed by the downloader. The root requirements file includes the pinned M5 dependencies and selects the PyTorch CPU wheel on Linux, using the official CPU package index. It does not install the older baseline environment. No system package file is required.

Only the four inference files are downloaded, on the first valid model request when local artifacts are missing. Downloads use a pinned commit and the model loader still checks the selected weight hash. A complete local model remains usable without Hub credentials. Files and the loaded model are reused on that instance; restarts or instance replacement can require downloading again. Do not rely on hosted local disk as permanent storage.

Official instructions: [PyTorch CPU installation](https://pytorch.org/get-started/previous-versions/), [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies), and [Hub snapshot downloads](https://huggingface.co/docs/huggingface_hub/package_reference/file_download).

## 3. Check the deployed app

Record the URL, deployment date, Git commit, Python version, and outcome of each check in [the performance report](performance/README.md).

| Check | Expected result |
|---|---|
| Open normally and with dark system appearance | White interface; no visible exception |
| Synthetic example and Analyse match | One of the three labels; human-review guidance |
| Blank fields | Analysis disabled |
| Punctuation-only or over 50,000 characters in either field | Correction message; text retained |
| Long valid input | Shortened-input notice and token counts |
| Edit after a prediction, then Clear | Old result removed; Clear resets fields |
| Incorrect model settings in a temporary test deployment | Safe unavailable message and reference; no label or token exposed |
| Correct settings, reboot test deployment, retry | Prediction succeeds |
| Narrow/mobile viewport | Readable stacked fields; no horizontal overflow |

Use synthetic text for deployment checks. Do not intentionally break a shared live app to test recovery; use a temporary test deployment.

## 4. Record hosted performance

The maintainer measurement view is enabled only while `PERFORMANCE_TOKEN` is configured. Use a long unique password. Open:

```text
https://YOUR_APP.streamlit.app/?performance=1
```

Enter the maintainer password and select **Measure performance**. Run while other people are not using the app, because it resets the shared model cache. Download `hosted_cpu.json` and send it back with the app URL and the completed checks above. This view uses synthetic text and displays environment, timings, and memory measurements; it never asks for resume records. Remove `PERFORMANCE_TOKEN` from Secrets after collecting results to disable the view.

The report separates model provision/hash/load time, the first request after loading, and 20 warm sequential requests. RSS is sampled every 10 ms for the whole process. Existing model references or other sessions can increase memory; use a freshly rebooted idle instance for a cleaner measurement. Streamlit/Python imports occur before timing starts. Download time is included only when model files are absent. It excludes browser rendering and network round trips. Separately record approximate click-to-result time on three browser requests and identify it as a manual measurement.

For local or shell-accessible hosting:

```bash
python -m m5.benchmark --repeats 20 --output m5/performance/local_cpu.json
```

Do not run this command alongside the test suite or other model benchmarks. Measurements describe one sequential synthetic workload, not concurrency capacity or a service guarantee.

## 5. Monitor and recover

Open Community Cloud's app management logs. Each request records a reference, event, character counts, and elapsed time, without document text, predicted labels, or exception details. Match a user-visible support reference to `request_id`.

- Repeated `model_load_failed`: verify model repository access, read token, pinned commit, exact files, and frozen weight hash. Retry after fixing configuration; reboot if necessary.
- Repeated `prediction_failed`: retry once, then check dependency versions and available memory. Reboot an unhealthy instance.
- Repeatedly slow `prediction_completed`: compare warm latency with the recorded baseline; check whether the instance was cold or handling other requests.
- Process killed or out of memory: inspect platform logs and restart. Python cannot safely catch every process-level failure. Reduce usage or move to a larger CPU host if the model does not fit.

Restrict access to platform logs and credentials. Review the platform's retention settings. No automated alerts, rate limiter, hard request timeout, or multi-user load guarantee is implemented. Shared inference serializes calls, and concurrent requests can queue. This is a demonstration with human review, not an automated hiring service.
