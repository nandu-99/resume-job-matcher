# Prototype performance and deployment record

## Status

Local integration is verified. Community Cloud deployment, Linux installation, private Hub download, public URL, hosted timings, and hosted acceptance checks remain pending. The maintainer publishes the app using the [deployment guide](../DEPLOYMENT.md), then supplies the downloaded hosted report and app URL. Do not mark issue #36 fully deployed before those checks pass.

## Local CPU measurements

Measured on 25 November 2026 in a fresh benchmark process, after the tests finished. [local_cpu.json](local_cpu.json) preserves the machine and package versions, selected weight hash, and measured values.

| Measurement | Local result |
|---|---:|
| Model verification and CPU load, files already present | 0.7306 s |
| First guarded prediction after loading | 217.763 ms |
| Warm sequential requests | 20 |
| Warm median request time | 29.219 ms |
| Warm P95 request time | 40.956 ms |
| Whole-process RSS before loading | 420.27 MiB |
| Sampled peak whole-process RSS | 535.91 MiB |

Environment: macOS ARM64, 8 logical CPUs, 4 PyTorch threads, Python 3.14.0, PyTorch 2.10.0, Transformers 5.3.0. The workload repeats the synthetic example included in the interface. It covers validation, preparation, original-length tokenization, truncated pair tokenization, CPU model inference, response validation, and metadata logging. Model provision/load is measured separately. Imports, UI rendering, and browser/network round trips are excluded. Download was not needed in this run.

Memory is sampled every 10 ms with psutil and may miss short peaks. These are whole-process measurements, not model weight size. A hosted Streamlit process can consume more memory because of framework state, caches, and sessions. One sequential workload on this laptop does not establish Cloud performance, concurrent capacity, or a response-time guarantee. Earlier M4 GPU timings measured a different scope and are not directly comparable.

## Verification

All 26 local tests passed. The local suite covers the inference pipeline, white interface behaviour, validation and safe failures, model provisioning configuration, and the protected deployment entry point. The model-dependent checks include agreement with all 30 saved M4 review predictions. This selected sample is not a new model evaluation. No training or official-test rerun was performed.

Private Hub transfer and Linux dependency installation have not been exercised locally. Provisioning tests substitute the download call to check the immutable revision, allowlisted files, local reuse, and credential handling without contacting an account. Hosted acceptance still needs a real download and prediction.

## Hosted deployment record

| Item | Result |
|---|---|
| App URL | Pending |
| Deployed Git commit and date | Pending |
| Hosting Python and package versions | Pending |
| Model repository commit and verified weight hash | Pending |
| First provision/hash/load time | Pending |
| First request after loading | Pending |
| Warm median and P95, 20 requests | Pending |
| Whole-process sampled peak RSS | Pending |
| Three manual browser click-to-result timings | Pending |
| White theme and mobile layout | Pending |
| Valid, empty, invalid, oversized, and truncated inputs | Pending |
| Stale-result clearing and model-failure recovery | Pending |

Download `hosted_cpu.json` from the protected measurement view and place it beside this report after review. Fill the table with actual results; do not copy laptop timings into it. Add the deployment Git commit because runtime package versions alone do not identify the application version. Remove the optional measurement password from Cloud Secrets after collection.

## Monitoring and limitations

Review the platform console for request failures and latency using the existing metadata events. Follow the [recovery instructions](../DEPLOYMENT.md#5-monitor-and-recover). No document text, predicted labels, credentials, or raw exceptions belong in operational logs. Automated alerts, hard timeouts, and public multi-user load testing are not implemented.

The app continues to use the checkpoint selected before M4 test evaluation. Its official-test macro-F1 is 0.3563 and suitable-candidate recall is low. The TF-IDF comparator achieved a higher test macro-F1. Deployment does not change those findings; users must review the complete documents and make the hiring decision themselves.
