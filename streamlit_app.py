"""Community Cloud entry point. Run from the repository root."""

import hmac
import os

import streamlit as st

from m5.app import main

# Streamlit root secrets are also environment variables; explicit access ensures
# they are available before the first model request, including local execution.
try:
    for name in ("RESUME_MATCHER_HF_REPO", "RESUME_MATCHER_HF_REVISION", "HF_TOKEN"):
        if name in st.secrets:
            os.environ[name] = str(st.secrets[name])
    performance_token = st.secrets.get("PERFORMANCE_TOKEN", "")
except FileNotFoundError:
    performance_token = ""

if st.query_params.get("performance") == "1" and performance_token:
    st.set_page_config(page_title="Prototype performance", layout="centered")
    st.title("Prototype performance")
    supplied = st.text_input("Maintainer password", type="password")
    if not hmac.compare_digest(supplied.encode(), str(performance_token).encode()):
        st.stop()
    st.caption("Synthetic CPU requests only. Run while the app is otherwise idle.")
    if st.button("Measure performance"):
        from m5.benchmark import run_benchmark
        import json

        try:
            with st.spinner("Measuring model loading and 20 requests..."):
                report = run_benchmark()
            st.json(report)
            st.download_button(
                "Download performance report", json.dumps(report, indent=2),
                file_name="hosted_cpu.json", mime="application/json",
            )
        except Exception:
            st.error("Measurement failed. Check model configuration and available memory, then retry.")
    st.stop()

main()
