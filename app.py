
import html
import streamlit as st

from resume_parser import extract_resume_text
from matcher import analyze_match
from ai_suggestions import generate_suggestions


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""

if "job_description_saved" not in st.session_state:
    st.session_state.job_description_saved = ""

if "resume_pages" not in st.session_state:
    st.session_state.resume_pages = 0

if "ai_suggestions" not in st.session_state:
    st.session_state.ai_suggestions = None

if "ai_error" not in st.session_state:
    st.session_state.ai_error = None


# ==========================================================
# DARK NAVY + VIOLET THEME
# ==========================================================

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --bg: #0B1020;
        --panel: #121A2B;
        --panel-hover: #19243A;
        --border: #29344B;
        --text: #F1F5F9;
        --muted: #A7B3C7;
        --violet: #8B5CF6;
        --violet-light: #C4B5FD;
        --success: #34D399;
        --warning: #FBBF24;
        --danger: #FCA5A5;
    }

    /* Keep the app's presentation consistent with our dark theme. */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 95% 0%,
                rgba(139, 92, 246, 0.12),
                transparent 38%
            ),
            var(--bg) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.96) !important;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Typography */
    h1, h2, h3, h4,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    label, .stCaption,
    [data-testid="stWidgetLabel"] p {
        color: var(--text) !important;
    }

    h1, h2, h3 {
        letter-spacing: -0.035em;
    }

    [data-testid="stCaptionContainer"] p,
    .stCaption {
        color: var(--muted) !important;
    }

    /* Hero */
    .hero {
        padding: 1.8rem;
        border: 1px solid var(--border);
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            rgba(139, 92, 246, 0.17),
            rgba(18, 26, 43, 0.98) 58%,
            rgba(30, 41, 59, 0.70)
        );
        margin-bottom: 1.3rem;
    }

    .hero-eyebrow, .section-label {
        color: var(--violet-light) !important;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .hero-eyebrow {
        margin-bottom: 0.7rem;
    }

    .hero-title {
        color: #F8FAFC !important;
        font-size: clamp(1.9rem, 4vw, 2.8rem);
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin: 0;
    }

    .hero-description {
        color: #C0CADD !important;
        font-size: 1rem;
        line-height: 1.75;
        margin-top: 0.9rem;
        max-width: 800px;
    }

    .section-label {
        margin: 0.7rem 0 0.4rem;
    }

    /* Cards */
    .panel, .metric-card {
        background: var(--panel) !important;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        margin-bottom: 0.8rem;
    }

    .metric-card {
        background: linear-gradient(
            145deg,
            #19243A,
            #121A2B
        ) !important;
        min-height: 125px;
    }

    .metric-label {
        color: var(--muted) !important;
        font-size: 0.82rem;
        font-weight: 650;
        margin-bottom: 0.55rem;
    }

    .metric-value {
        color: #F8FAFC !important;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }

    .metric-caption {
        color: var(--muted) !important;
        font-size: 0.78rem;
        margin-top: 0.5rem;
    }

    /* Notices */
    .notice {
        padding: 0.95rem 1.05rem;
        border-radius: 12px;
        background: rgba(139, 92, 246, 0.09);
        border: 1px solid rgba(139, 92, 246, 0.28);
        color: #DDD6FE !important;
        font-size: 0.87rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }

    .footer {
        color: #94A3B8 !important;
        font-size: 0.8rem;
        line-height: 1.7;
        padding-top: 0.8rem;
    }

    /* Form */
    div[data-testid="stForm"] {
        background: rgba(18, 26, 43, 0.85) !important;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.25rem;
    }

    div[data-testid="stFileUploader"] section {
        background: #0F172A !important;
        border: 1px dashed #4B5873 !important;
        border-radius: 12px;
    }

    div[data-testid="stFileUploader"] section * {
        color: var(--text) !important;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        background: #0F172A !important;
        color: #F1F5F9 !important;
        border: 1px solid #35415B !important;
        border-radius: 10px;
        caret-color: #C4B5FD;
    }

    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #8491A7 !important;
        opacity: 1;
    }

    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--violet) !important;
        box-shadow: 0 0 0 1px var(--violet) !important;
    }

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button,
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(196, 181, 253, 0.45) !important;
        border-radius: 10px;
        font-weight: 700;
        min-height: 2.7rem;
        transition: border-color 0.2s ease, filter 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        border-color: #DDD6FE !important;
        filter: brightness(1.12);
    }

    .stButton > button:focus-visible,
    .stFormSubmitButton > button:focus-visible {
        outline: 2px solid #C4B5FD !important;
        outline-offset: 2px;
    }

    /* Metrics and progress */
    [data-testid="stMetric"] {
        background: transparent !important;
    }

    [data-testid="stMetric"] label,
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: var(--text) !important;
    }

    [data-testid="stProgress"] > div > div {
        background-color: var(--violet) !important;
    }

    /* Tabs */
    [data-testid="stTabs"] button {
        color: #C0CADD !important;
        font-weight: 650;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--violet-light) !important;
    }

    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: var(--violet) !important;
    }

    /* Expander and code/text areas */
    [data-testid="stExpander"] {
        background: var(--panel) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color: var(--text) !important;
    }

    [data-testid="stCode"],
    [data-testid="stCodeBlock"] {
        background: #0F172A !important;
    }

    /* Keep alerts legible */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    /* ===== THEME VISIBILITY PATCH ===== */

    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #0B1020 !important;
        color: #F1F5F9 !important;
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #F1F5F9 !important;
    }

    [data-testid="stTabs"] button {
        color: #C0CADD !important;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #C4B5FD !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #A7B3C7 !important;
    }
    hr {
        border-color: var(--border) !important;
    }

    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 1rem 2rem;
        }

        .hero {
            padding: 1.25rem;
        }

        .metric-card {
            min-height: auto;
        }

        div[data-testid="stForm"] {
            padding: 0.85rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# REUSABLE UI HELPERS
# ==========================================================

def render_chips(items, kind="default"):
    """Render safely escaped skill or keyword chips."""
    if not items:
        st.caption("No items to display.")
        return

    css_class = {
        "default": "skill-chip",
        "matched": "skill-chip matched-chip",
        "missing": "skill-chip missing-chip",
    }.get(kind, "skill-chip")

    chips = "".join(
        f'<span class="{css_class}">{html.escape(str(item))}</span>'
        for item in items
    )

    st.markdown(
        f"""
        <style>
        .skill-chip {{
            display: inline-block;
            padding: 0.38rem 0.68rem;
            margin: 0.2rem 0.25rem 0.2rem 0;
            border-radius: 8px;
            background: rgba(139, 92, 246, 0.12);
            border: 1px solid rgba(139, 92, 246, 0.30);
            color: #DDD6FE !important;
            font-size: 0.84rem;
            overflow-wrap: anywhere;
        }}
        .matched-chip {{
            background: rgba(52, 211, 153, 0.08);
            border-color: rgba(52, 211, 153, 0.28);
            color: #A7F3D0 !important;
        }}
        .missing-chip {{
            background: rgba(251, 191, 36, 0.08);
            border-color: rgba(251, 191, 36, 0.28);
            color: #FDE68A !important;
        }}
        </style>
        {chips}
        """,
        unsafe_allow_html=True,
    )


def render_metric(label, value, caption=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-caption">{html.escape(str(caption))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">AI-powered career toolkit</div>
        <div class="hero-title">
            Resume Analyzer <span style="color:#A78BFA;">&amp;</span>
            Job Matcher
        </div>
        <div class="hero-description">
            See how your resume aligns with a target role.
            Discover skill gaps, compare important keywords, and get
            practical suggestions to improve your application.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="notice">
        <strong>Important:</strong> The similarity score is a text-based
        estimate, not an official ATS score or a prediction of hiring
        success. AI suggestions may be imperfect. Verify every suggested
        change and never include qualifications or experience you do not have.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# INPUT FORM
# ==========================================================

st.markdown(
    '<div class="section-label">01 / YOUR APPLICATION</div>',
    unsafe_allow_html=True,
)
st.subheader("Upload and compare")
st.caption("Upload a text-based PDF and paste the target job description.")

with st.form("resume_analysis_form", clear_on_submit=False):
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("**Your resume**")
        resume_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            help="Only PDF files are supported. Password-protected or scanned PDFs may not work.",
            key="resume_upload",
        )
        st.caption("PDF only · Processed for this analysis.")

    with right:
        st.markdown("**Target job description**")
        job_description = st.text_area(
            "Paste the job description",
            height=190,
            placeholder=(
                "Paste the job title, responsibilities, required skills "
                "and eligibility criteria here..."
            ),
            label_visibility="collapsed",
            key="job_description_input",
        )

    submitted = st.form_submit_button(
        "Analyze resume",
        type="primary",
        use_container_width=True,
    )


# ==========================================================
# ANALYSIS AND VALIDATION
# ==========================================================

if submitted:
    if resume_file is None:
        st.error("Please upload a PDF resume before continuing.")
        st.stop()

    if not job_description or not job_description.strip():
        st.error("Please paste the target job description before continuing.")
        st.stop()

    if not resume_file.name.lower().endswith(".pdf"):
        st.error("Please upload a valid PDF file.")
        st.stop()

    try:
        with st.spinner("Reading your resume and comparing it with the role..."):
            pdf_bytes = resume_file.getvalue()

            resume_text, page_count = extract_resume_text(pdf_bytes)

            if not resume_text or not resume_text.strip():
                st.error(
                    "No readable text was found. Please upload a text-based PDF."
                )
                st.stop()

            result = analyze_match(
                resume_text,
                job_description.strip(),
            )

        # Save successful analysis in session state so results
        # remain visible during normal Streamlit reruns.
        st.session_state.analysis_result = result
        st.session_state.resume_text = resume_text
        st.session_state.resume_name = resume_file.name
        st.session_state.resume_pages = page_count
        st.session_state.job_description_saved = job_description.strip()

        # Generate AI suggestions separately so Gemini failures do not
        # remove the successful similarity and matching results.
        st.session_state.ai_suggestions = None
        st.session_state.ai_error = None

        try:
            with st.spinner("Generating personalized AI suggestions..."):
                st.session_state.ai_suggestions = generate_suggestions(
                    resume_text,
                    job_description.strip(),
                )
        except Exception as exc:
            # Do not display secrets or internal exception details.
            st.session_state.ai_error = (
                "AI suggestions are temporarily unavailable. "
                "Your resume matching results are still ready. "
                "Check your Gemini API configuration or try again later."
            )
            print("AI suggestions error type:", type(exc).__name__)

        st.success("Resume analysis completed.")

    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.error(
            "Something went wrong while analyzing the resume. "
            "Please check the PDF and try again."
        )
        print("Resume analysis error type:", type(exc).__name__)
        st.stop()


# ==========================================================
# RESULTS DASHBOARD
# ==========================================================

result = st.session_state.analysis_result

if result is not None:
    st.divider()

    st.markdown(
        '<div class="section-label">02 / MATCH OVERVIEW</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Your results")

    st.caption(
        f"Resume: {st.session_state.resume_name} · "
        f"{st.session_state.resume_pages} page(s)"
    )

    score = float(result.get("score", 0))
    score = max(0.0, min(100.0, score))

    matched_skills = result.get("matched_skills", [])
    missing_skills = result.get("missing_skills", [])
    resume_skills = result.get("resume_skills", [])
    job_skills = result.get("job_skills", [])
    matched_keywords = result.get("matched_keywords", [])
    missing_keywords = result.get("missing_keywords", [])

    skill_total = len(matched_skills) + len(missing_skills)
    skill_coverage = (
        len(matched_skills) / skill_total * 100
        if skill_total
        else 0
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        render_metric(
            "Text similarity",
            f"{score:.1f}%",
            "TF-IDF and cosine similarity",
        )

    with col2:
        render_metric(
            "Matched skills",
            f"{len(matched_skills)} / {skill_total}",
            "Recognized skills shared with the role",
        )

    with col3:
        render_metric(
            "Matched keywords",
            str(len(matched_keywords)),
            f"{len(missing_keywords)} extracted keywords not found",
        )

    st.markdown("**Recognized skill coverage**")
    st.progress(int(round(skill_coverage)))
    st.caption(
        f"{skill_coverage:.1f}% of the recognized job-description skills "
        "were also found in your resume."
    )

    st.markdown(
        """
        <div class="notice">
            Similarity and skill coverage measure different things.
            A higher similarity score does not guarantee an interview.
            Missing items are prompts for review, not automatic recommendations
            to add skills you do not possess.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # DETAILED RESULTS TABS
    # ------------------------------------------------------

    overview_tab, skills_tab, keywords_tab, ai_tab, text_tab = st.tabs(
        [
            "Overview",
            "Skills",
            "Keywords",
            "AI Suggestions",
            "Extracted Text",
        ]
    )

    with overview_tab:
        st.markdown("### Match summary")

        overview_left, overview_right = st.columns(2, gap="large")

        with overview_left:
            st.markdown("**Skills found in your resume**")
            render_chips(resume_skills, "default")

        with overview_right:
            st.markdown("**Skills identified in the job description**")
            render_chips(job_skills, "default")

        st.markdown("### Recommended focus")

        if missing_skills:
            st.warning(
                f"Review {len(missing_skills)} skill(s) that were not "
                "detected in your resume. Add them only if you genuinely "
                "have the relevant knowledge or experience."
            )
            render_chips(missing_skills, "missing")
        else:
            st.success(
                "All recognized job-description skills were found in your resume."
                if job_skills
                else "No skills from the supported recognition list were detected in the job description."
            )

        if missing_keywords:
            st.markdown("**Keywords worth reviewing**")
            render_chips(missing_keywords[:12], "missing")

    with skills_tab:
        st.markdown("### Skill comparison")
        skill_left, skill_right = st.columns(2, gap="large")

        with skill_left:
            st.markdown("**Matched skills**")
            st.caption("Found in both the resume and job description.")
            render_chips(matched_skills, "matched")

        with skill_right:
            st.markdown("**Skills not detected in resume**")
            st.caption("Review these against your actual experience.")
            render_chips(missing_skills, "missing")

        with st.expander("View all skills detected in your resume"):
            render_chips(resume_skills, "default")

        with st.expander("View all skills detected in the job description"):
            render_chips(job_skills, "default")

    with keywords_tab:
        st.markdown("### Job-description keyword comparison")
        keyword_left, keyword_right = st.columns(2, gap="large")

        with keyword_left:
            st.markdown("**Keywords found in resume**")
            render_chips(matched_keywords, "matched")

        with keyword_right:
            st.markdown("**Keywords not found in resume**")
            render_chips(missing_keywords, "missing")

        st.caption(
            "Keywords are extracted using TF-IDF from the supplied job "
            "description. They are useful indicators, not a definitive ATS checklist."
        )

    with ai_tab:
        st.markdown("### Personalized improvement suggestions")

        if st.session_state.ai_suggestions:
            st.markdown(st.session_state.ai_suggestions)

        elif st.session_state.ai_error:
            st.warning(st.session_state.ai_error)

            if st.button("Retry AI suggestions", key="retry_ai"):
                try:
                    with st.spinner("Requesting suggestions from Gemini..."):
                        suggestions = generate_suggestions(
                            st.session_state.resume_text,
                            st.session_state.job_description_saved,
                        )

                    st.session_state.ai_suggestions = suggestions
                    st.session_state.ai_error = None
                    st.rerun()

                except Exception as exc:
                    st.session_state.ai_error = (
                        "Gemini could not generate suggestions right now. "
                        "Please check the API key, model availability, "
                        "quota and network connection."
                    )
                    print("Gemini retry error type:", type(exc).__name__)
                    st.error(st.session_state.ai_error)

        else:
            st.info("AI suggestions have not been generated for this analysis.")

        st.caption(
            "Review every suggestion carefully. Do not invent experience, "
            "achievements, metrics, or qualifications."
        )

    with text_tab:
        st.markdown("### Extracted resume text")
        st.caption(
            "Check this text to confirm that the PDF was read correctly."
        )

        with st.expander("Show extracted text", expanded=False):
            st.text(st.session_state.resume_text)

        st.download_button(
            "Download extracted text",
            data=st.session_state.resume_text,
            file_name="extracted_resume_text.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # ------------------------------------------------------
    # DOWNLOAD ANALYSIS SUMMARY
    # ------------------------------------------------------

    st.divider()
    st.markdown("### Export your results")

    summary_lines = [
        "AI Resume Analyzer & Job Matcher",
        f"Resume: {st.session_state.resume_name}",
        f"Text similarity: {score:.1f}%",
        f"Matched skills: {', '.join(matched_skills) or 'None detected'}",
        f"Missing skills: {', '.join(missing_skills) or 'None detected'}",
        f"Matched keywords: {', '.join(matched_keywords) or 'None detected'}",
        f"Missing keywords: {', '.join(missing_keywords) or 'None detected'}",
        "",
        "Note: This is a text-based estimate, not an official ATS score.",
    ]

    if st.session_state.ai_suggestions:
        summary_lines.extend(
            [
                "",
                "AI SUGGESTIONS",
                st.session_state.ai_suggestions,
            ]
        )

    st.download_button(
        "Download analysis summary",
        data="\n".join(summary_lines),
        file_name="resume_analysis.txt",
        mime="text/plain",
        use_container_width=True,
    )

    if st.button("Clear results", key="clear_results"):
        st.session_state.analysis_result = None
        st.session_state.resume_text = ""
        st.session_state.resume_name = ""
        st.session_state.job_description_saved = ""
        st.session_state.resume_pages = 0
        st.session_state.ai_suggestions = None
        st.session_state.ai_error = None
        st.rerun()

else:
    st.markdown(
        """
        <div class="panel">
            <div class="section-label">HOW IT WORKS</div>
            <p><strong>01 · Upload</strong> — Select your text-based PDF resume.</p>
            <p><strong>02 · Compare</strong> — Paste the job description and run the analysis.</p>
            <p><strong>03 · Improve</strong> — Review similarity, skill gaps, keywords and AI suggestions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# PRIVACY NOTICE AND FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <strong>Privacy notice:</strong> Resume text is processed by this
        application for analysis. When AI suggestions are requested, resume
        text and the job description are sent to the configured Gemini API.
        Avoid uploading sensitive information that is not needed for the task.
        This app does not intentionally save uploaded resumes to a separate
        file, but data may remain in the active Streamlit session until cleared
        or the session ends. Review your hosting and API provider's data policies
        before deploying this application publicly.
        <br><br>
        AI Resume Analyzer &amp; Job Matcher · Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
