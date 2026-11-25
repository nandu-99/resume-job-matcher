"""Run from the repository root with: streamlit run m5/app.py."""

from pathlib import Path

import streamlit as st

from m5.service import MatchError, analyse_match
from m5.validation import InputValidationError, MAX_INPUT_CHARACTERS


EXAMPLE_RESUME = """Software developer with five years of backend development experience.
Skills: Python, SQL, PostgreSQL, REST APIs, Git, and Docker.
Experience: Built data-processing services, maintained APIs, and wrote automated tests.
Education: Bachelor's degree in Computer Science."""

EXAMPLE_JOB = """Backend Software Developer
Develop and maintain Python services and REST APIs.
Requirements: Three years of backend development, strong SQL skills, Git,
automated testing, and experience with relational databases.
Docker experience is preferred."""

RESULT_COPY = {
    "Good Fit": "The model predicts a good fit. Confirm the key requirements against the full documents.",
    "Potential Fit": "The model predicts a potential fit. Review the relevant experience and any gaps.",
    "No Fit": "The model predicts no fit. Review the full documents before ruling out the candidate.",
}


def clear_result():
    st.session_state["match_result"] = None
    st.session_state["match_error"] = None
    st.session_state["match_error_reference"] = None


def use_example():
    st.session_state["resume_text"] = EXAMPLE_RESUME
    st.session_state["job_text"] = EXAMPLE_JOB
    clear_result()


def clear_inputs():
    st.session_state["resume_text"] = ""
    st.session_state["job_text"] = ""
    clear_result()


def main():
    st.set_page_config(
        page_title="Resume-job matcher",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    stylesheet = Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)

    for key, default in {
        "resume_text": "", "job_text": "",
        "match_result": None, "match_error": None, "match_error_reference": None,
    }.items():
        st.session_state.setdefault(key, default)

    st.title("Resume-job matcher")
    st.write("Compare a candidate's experience with the role you're hiring for.")
    st.caption("A prediction to support your review. The hiring decision stays with you.")

    with st.container(horizontal=True, gap="small", key="input_actions"):
        st.button("Use an example", key="use_example", on_click=use_example)
        st.button("Clear", key="clear_inputs", on_click=clear_inputs)

    with st.container(key="input_columns"):
        resume_column, job_column = st.columns(2, gap="large")
        with resume_column:
            resume = st.text_area(
                "Resume", key="resume_text", height=280,
                placeholder="Paste the candidate's experience, skills, and education...",
                on_change=clear_result,
            )
            st.caption(
                f"{len(resume):,} / {MAX_INPUT_CHARACTERS:,} characters. "
                "Include experience, skills, and education."
            )
        with job_column:
            job = st.text_area(
                "Job description", key="job_text", height=280,
                placeholder="Paste the role, responsibilities, and required qualifications...",
                on_change=clear_result,
            )
            st.caption(
                f"{len(job):,} / {MAX_INPUT_CHARACTERS:,} characters. "
                "Include responsibilities and required qualifications."
            )

    ready = bool(resume.strip() and job.strip())
    if st.button(
        "Analyse match", type="primary", key="analyse_match", disabled=not ready,
    ):
        clear_result()
        try:
            with st.spinner("Analysing the resume and job description..."):
                st.session_state["match_result"] = analyse_match(resume, job)
        except InputValidationError as error:
            st.session_state["match_error"] = str(error)
        except MatchError as error:
            st.session_state["match_error"] = str(error)
            st.session_state["match_error_reference"] = error.request_id

    if not ready:
        st.caption("Add both texts to enable analysis.")

    result = st.session_state["match_result"]
    error = st.session_state["match_error"]

    with st.container(border=True, key="result_panel"):
        st.caption("Match result")
        if error:
            st.error(error)
            if st.session_state["match_error_reference"]:
                st.caption(f"Reference: {st.session_state['match_error_reference']}")
        elif result:
            st.subheader(result["label"])
            st.write(RESULT_COPY[result["label"]])
            if result["truncated"]:
                st.markdown(
                    "**Long input was shortened.** Only part of the supplied text was processed. "
                    "Review the complete documents before deciding."
                )
                st.caption(
                    f"Input coverage: {result['input_tokens']:,} of "
                    f"{result['original_tokens']:,} prepared tokens."
                )
            else:
                st.caption("Both inputs fit within the model's input limit.")
        else:
            st.subheader("Your result will appear here")
            st.write("Add both texts, then select Analyse match.")

    with st.expander("About this tool"):
        st.write(
            "This prototype predicts Good Fit, Potential Fit, or No Fit. It can miss suitable "
            "candidates and is sensitive to document structure and long inputs. "
            "It does not explain individual skill matches or provide a calibrated match percentage."
        )
        st.write(
            "Use the prediction alongside your own assessment. Text and results remain in this "
            "session's memory; the interface does not save document text or results to files or logs. "
            "Clear removes them from the active interface."
        )
        st.caption(
            "Operational logs contain a request reference, outcome, character counts, "
            "and elapsed time. They exclude document text, predictions, and exception details."
        )


if __name__ == "__main__":
    main()
