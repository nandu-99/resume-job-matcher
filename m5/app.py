"""Run from the repository root with: streamlit run streamlit_app.py."""

from pathlib import Path

import streamlit as st

from m5.service import MatchError, analyse_match
from m5.pdf_input import PDFInputError, extract_pdf
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


# Editing either document invalidates the previous prediction.
def clear_result():
    st.session_state["match_result"] = None
    st.session_state["match_error"] = None
    st.session_state["match_error_reference"] = None


def reset_uploads():
    st.session_state["upload_generation"] = st.session_state.get("upload_generation", 0) + 1
    for prefix in ("resume", "job"):
        st.session_state[f"{prefix}_source"] = "Paste text"
        st.session_state[f"{prefix}_pdf_report"] = None
        st.session_state[f"{prefix}_pdf_error"] = None


def invalidate_document(prefix):
    st.session_state[f"{prefix}_text"] = ""
    st.session_state[f"{prefix}_pdf_report"] = None
    st.session_state[f"{prefix}_pdf_error"] = None
    clear_result()


def use_example():
    reset_uploads()
    st.session_state["resume_text"] = EXAMPLE_RESUME
    st.session_state["job_text"] = EXAMPLE_JOB
    clear_result()


def clear_inputs():
    reset_uploads()
    st.session_state["resume_text"] = ""
    st.session_state["job_text"] = ""
    clear_result()


def begin_analysis():
    clear_result()
    st.session_state["pending_action"] = {"kind": "analyse"}


def begin_pdf(prefix, uploaded, force_ocr):
    if uploaded is None:
        return
    invalidate_document(prefix)
    st.session_state["pending_action"] = {
        "kind": "pdf", "prefix": prefix,
        "content": uploaded.getvalue(), "force_ocr": force_ocr,
    }


def document_ready(prefix):
    return (
        st.session_state[f"{prefix}_source"] == "Paste text"
        or st.session_state.get(f"{prefix}_pdf_report") is not None
    )


def pdf_controls(prefix, busy):
    report = st.session_state.get(f"{prefix}_pdf_report")
    generation = st.session_state["upload_generation"]
    with st.container(horizontal=True, vertical_alignment="center", gap="small", key=f"{prefix}_source_row"):
        with st.popover(
            "PDF source" if report else "Choose PDF", disabled=busy,
            key=f"{prefix}_pdf_controls_{bool(report)}_{busy}",
        ):
            uploaded = st.file_uploader(
                "Choose PDF", type=["pdf"], key=f"{prefix}_pdf_{generation}",
                max_upload_size=10, on_change=invalidate_document, args=(prefix,),
                label_visibility="collapsed", disabled=busy,
            )
            force_ocr = st.checkbox(
                "Use OCR on every page", key=f"{prefix}_ocr_{generation}",
                on_change=invalidate_document, args=(prefix,), disabled=busy,
                help="Use if automatic reading misses scanned content or produces unreadable text",
            )
            st.button(
                "Read PDF", key=f"{prefix}_read_pdf", disabled=busy or uploaded is None,
                on_click=begin_pdf, args=(prefix, uploaded, force_ocr),
            )
            st.caption("English PDFs / up to 10 MB / up to 10 pages")
        if report:
            page_word = "page" if report.pages == 1 else "pages"
            method = f"OCR on {len(report.ocr_pages)}" if report.ocr_pages else "Embedded text"
            st.caption(f"{report.pages} {page_word} / {method}")
        else:
            st.caption("Read a PDF, then review its text")
    if st.session_state.get(f"{prefix}_pdf_error"):
        st.error(st.session_state[f"{prefix}_pdf_error"])
    if report and report.empty_pages:
        pages = ", ".join(map(str, report.empty_pages))
        st.warning(f"No readable text on page(s) {pages}. Add any missing content below.")
    return report


def document_panel(prefix, title, number, busy):
    text = st.session_state[f"{prefix}_text"]
    ready = bool(text.strip() and document_ready(prefix))
    status = "Text ready" if ready else "Awaiting document"
    with st.container(border=True, key=f"{prefix}_panel"):
        st.markdown(
            f'<div class="document-heading"><span class="document-number">{number}</span>'
            f'<h2>{title}</h2><span class="document-state {"is-ready" if ready else "is-waiting"}">{status}</span></div>',
            unsafe_allow_html=True,
        )
        st.radio(
            f"{title} input method", ("Paste text", "Upload PDF"),
            key=f"{prefix}_source", horizontal=True, label_visibility="collapsed",
            on_change=invalidate_document, args=(prefix,), disabled=busy,
        )
        uploaded_mode = st.session_state[f"{prefix}_source"] == "Upload PDF"
        if uploaded_mode:
            report = pdf_controls(prefix, busy)
        else:
            report = None
            with st.container(horizontal=True, vertical_alignment="center", key=f"{prefix}_source_row"):
                st.caption("Include experience and skills" if prefix == "resume" else "Include responsibilities and requirements")
        unread_pdf = uploaded_mode and report is None
        placeholder = (
            "Read your PDF to review its text here" if unread_pdf else
            "Experience, skills and education..." if prefix == "resume" else
            "Role, responsibilities and requirements..."
        )
        text = st.text_area(
            title, key=f"{prefix}_text", height=160,
            label_visibility="collapsed", placeholder=placeholder,
            on_change=clear_result, disabled=busy or unread_pdf,
        )
        st.caption(f"{len(text):,} / {MAX_INPUT_CHARACTERS:,} characters")

    return st.session_state[f"{prefix}_text"]


# Render the busy state first, then extract a PDF or call the matching service.
def run_pending_action():
    pending = st.session_state["pending_action"]
    if not pending:
        return
    try:
        if pending["kind"] == "pdf":
            name = "resume" if pending["prefix"] == "resume" else "job description"
            with st.status(f"Reading {name} PDF...", expanded=True) as status:
                st.write("Extracting text and reading scanned pages where needed")
                st.caption("Keep this tab open. Longer scans can take up to a minute.")
                try:
                    report = extract_pdf(pending["content"], force_ocr=pending["force_ocr"])
                    st.session_state["pdf_text_update"] = (pending["prefix"], report.text)
                    st.session_state[f"{pending['prefix']}_pdf_report"] = report
                    status.update(label="Document ready for review", state="complete", expanded=False)
                except PDFInputError as error:
                    st.session_state[f"{pending['prefix']}_pdf_error"] = str(error)
                    status.update(label="Document could not be read", state="error")
        else:
            with st.status("Analysing match...", expanded=True) as status:
                st.write("Preparing both documents and running the matching model")
                st.caption("The first analysis may take longer while the model loads")
                try:
                    st.session_state["match_result"] = analyse_match(
                        st.session_state["resume_text"], st.session_state["job_text"],
                    )
                    status.update(label="Analysis complete", state="complete", expanded=False)
                except InputValidationError as error:
                    st.session_state["match_error"] = str(error)
                    status.update(label="Check your documents", state="error")
                except MatchError as error:
                    st.session_state["match_error"] = str(error)
                    st.session_state["match_error_reference"] = error.request_id
                    status.update(label="Analysis could not finish", state="error")
    finally:
        st.session_state["pending_action"] = None
    st.rerun()


# Show the predicted class and coverage notice; no calibrated match percentage is available.
def result_panel():
    with st.container(border=True, key="result_panel"):
        content = st.empty()
        content.empty()
        with content.container():
            if st.session_state["pending_action"]:
                run_pending_action()
                return
            result = st.session_state["match_result"]
            error = st.session_state["match_error"]
            tone = {"Good Fit": "good", "Potential Fit": "potential", "No Fit": "no-fit"}.get(
                result["label"] if result else "", "empty"
            )
            if error:
                tone = "error"
            st.markdown(
                f'<div class="result-meta result-tone-{tone}"><span>Match result</span>'
                f'<span>{"Model prediction" if result and not error else "Document review"}</span></div>',
                unsafe_allow_html=True,
            )
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
                        f"{result['original_tokens']:,} prepared tokens"
                    )
                else:
                    st.caption("Both inputs fit within the model's input limit")
            else:
                st.subheader("Your result will appear here")
                st.write("Add both documents, review the text, then analyse the match.")


def main():
    st.set_page_config(page_title="Resume-job matcher", layout="wide", initial_sidebar_state="collapsed")
    stylesheet = Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
    for key, default in {
        "resume_text": "", "job_text": "", "resume_source": "Paste text",
        "job_source": "Paste text", "upload_generation": 0, "pending_action": None,
        "match_result": None, "match_error": None, "match_error_reference": None,
    }.items():
        st.session_state.setdefault(key, default)
    update = st.session_state.pop("pdf_text_update", None)
    if update:
        st.session_state[f"{update[0]}_text"] = update[1]
    busy = st.session_state["pending_action"] is not None
    if busy:
        # Streamlit can retain stale elements until a long-running rerun ends.
        stylesheet += (
            ".st-key-result_panel h3, "
            ".st-key-result_panel [data-stale='true'] {display:none !important;}"
        )
    st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)
    with st.container(key="page_heading"):
        heading, actions = st.columns([3, 2], vertical_alignment="center", gap="small")
        with heading:
            st.title("Resume-job matcher")
            st.write("Review a candidate's experience against the role")
        with actions:
            with st.container(horizontal=True, horizontal_alignment="right", gap="small", key="input_actions"):
                st.button("Use an example", key="use_example", on_click=use_example, disabled=busy)
                st.button("Clear", key="clear_inputs", on_click=clear_inputs, disabled=busy)
    with st.container(key="input_columns"):
        resume_column, job_column = st.columns(2, gap="medium")
        with resume_column:
            resume = document_panel("resume", "Resume", "1", busy)
        with job_column:
            job = document_panel("job", "Job description", "2", busy)
    ready = bool(resume.strip() and job.strip() and document_ready("resume") and document_ready("job"))
    with st.container(horizontal=True, vertical_alignment="center", gap="medium", key="analysis_actions"):
        st.button(
            ("Reading PDF..." if busy and st.session_state["pending_action"]["kind"] == "pdf"
             else "Analysing..." if busy else "Analyse match"),
            type="primary", key="analyse_match",
            disabled=busy or not ready, on_click=begin_analysis,
        )
        if busy:
            st.caption("Reading your document" if st.session_state["pending_action"]["kind"] == "pdf" else "Please keep this tab open")
        elif ready:
            st.caption("Both documents are ready / The hiring decision stays with you")
        else:
            st.caption("Add both documents to begin")
    result_panel()
    with st.expander("About this tool and your privacy"):
        st.write(
            "This prototype predicts Good Fit, Potential Fit, or No Fit. It can miss suitable "
            "candidates and is sensitive to document structure and long inputs. Review full documents "
            "before deciding. It does not explain individual skills or provide a calibrated match percentage."
        )
        st.write(
            "English printed PDFs are supported, including scans. OCR can misread text and column order; "
            "check the extracted text. Text and results stay in session memory. PDFs and OCR are processed "
            "on this app's server without an external OCR service or application document files. "
            "Clear removes them from the active interface."
        )
        st.caption(
            "Operational logs contain a request reference, outcome, character counts and elapsed time. "
            "They exclude document text, predictions and exception details."
        )


if __name__ == "__main__":
    main()
