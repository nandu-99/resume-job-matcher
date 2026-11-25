# Prototype performance and deployment record

## Status

The maintainer deployed the app at [resume-job-matcher-nlp.streamlit.app](https://resume-job-matcher-nlp.streamlit.app/) and supplied a successful Linux CPU benchmark on 25 November 2026. The reported model hash matches the frozen M4 selection. Local integration and hosted service inference have supporting evidence. Browser acceptance checks, exact deployed Git commit, and manual click-to-result timings still need confirmation before closing issue #36.

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

Provisioning unit tests substitute the download call to check the immutable revision, allowlisted files, local reuse, and credential handling. The maintainer-supplied hosted report now confirms that the deployed Linux runtime loaded the selected weights and completed 21 synthetic service predictions (one first request and 20 timed warm requests). The report does not separately record an initial Hub transfer, browser behaviour, or the deployed application Git commit.

## Hosted deployment record

| Item | Result |
|---|---|
| App URL | [Live application](https://resume-job-matcher-nlp.streamlit.app/) |
| Report received | 25 November 2026; supplied by maintainer in chat |
| Deployed Git commit and deployment date | Pending confirmation; not included in the benchmark |
| Hosting Python and packages | Python 3.14.10; torch 2.10.0+cpu; transformers 5.3.0; tokenizers 0.22.2; Streamlit 1.67.0; huggingface-hub 1.7.2; psutil 7.2.2 |
| Reported hardware | Linux x86_64; 16 visible logical CPUs; 8 PyTorch threads; these counts do not establish dedicated CPU allocation |
| Configured model repository revision | `pottabathini99/resume-job-matcher-weighted` at `c71888d7468f4ea943160c5eee341d20a77c9be1`, from maintainer setup; not captured in benchmark |
| Verified weight hash | `004d162ccc9daa4311ff9edeecb1e860a3638a5d0e0c530f5a929df7a40d4b72`, matches frozen M4 selection |
| Reported provision/hash/load duration | 0.3438 s; initial download or cold instance startup not established |
| First request after loading | 85.603 ms |
| Warm median and P95, 20 requests | 63.812 ms median; 147.603 ms P95 |
| Warm mean | 80.443 ms |
| Whole-process RSS baseline and sampled peak | 689.16 MiB baseline; 689.85 MiB peak |
| Three manual browser click-to-result timings | Pending |
| White theme and mobile layout | Pending hosted confirmation |
| Valid, empty, invalid, oversized, and truncated inputs | Synthetic service requests passed; browser checks pending |
| Stale-result clearing and model-failure recovery | Pending hosted confirmation |

[hosted_cpu.json](hosted_cpu.json) preserves the supplied benchmark values. These results exclude browser/network/rendering and Python imports. The memory baseline is already close to the sampled peak, so this is not evidence of total cold-start allocation or of the model needing only their difference. Cached files, allocator reuse, other model references, or sessions can affect the run. Do not describe the reported 0.3438 seconds as a first-download or complete app startup measurement.

No multi-user capacity or availability guarantee follows from this sequential synthetic workload. The app URL and report were supplied by the maintainer; automated browsing could not independently open the live app. Fill the remaining acceptance items with actual checks. Once measurement is finished, remove `PERFORMANCE_TOKEN` from Cloud Secrets to disable the maintainer measurement view.

## Monitoring and limitations

Review the platform console for request failures and latency using the existing metadata events. Follow the [recovery instructions](../DEPLOYMENT.md#5-monitor-and-recover). No document text, predicted labels, credentials, or raw exceptions belong in operational logs. Automated alerts, hard timeouts, and public multi-user load testing are not implemented.

The app continues to use the checkpoint selected before M4 test evaluation. Its official-test macro-F1 is 0.3563 and suitable-candidate recall is low. The TF-IDF comparator achieved a higher test macro-F1. Deployment does not change those findings; users must review the complete documents and make the hiring decision themselves.

## PDF and OCR addition

PDF upload and English neural OCR were added after the hosted measurement above. Those measurements remain historical text-service evidence and do not include upload, rendering, OCR latency, or worker memory. See the [PDF guide](../PDF_INPUT.md) and repeat hosted checks with synthetic text and scanned PDFs after deploying the new system packages.
