import streamlit as st
import pandas as pd
import time
from scorer import (
    get_match_score,
    get_missing_keywords,
    get_matching_keywords,
    get_score_label,
    get_improvement_tips,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Match Scorer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global font + background */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Hide default Streamlit header/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Score circle */
.score-circle {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    margin: 0 auto 1rem auto;
    font-size: 2.6rem;
    font-weight: 700;
    border: 6px solid;
}
.score-excellent { border-color: #1D9E75; color: #1D9E75; background: #f0fdf8; }
.score-good      { border-color: #378ADD; color: #378ADD; background: #eff6ff; }
.score-moderate  { border-color: #EF9F27; color: #EF9F27; background: #fffbeb; }
.score-low       { border-color: #E24B4A; color: #E24B4A; background: #fff1f1; }

/* Keyword pills */
.pill-container { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.pill-match   { background:#E1F5EE; color:#085041; padding:4px 12px; border-radius:20px; font-size:13px; font-weight:500; }
.pill-missing { background:#FAEEDA; color:#633806; padding:4px 12px; border-radius:20px; font-size:13px; font-weight:500; }

/* Tip cards */
.tip-card {
    background: #f8f9fa;
    border-left: 3px solid #1D9E75;
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 8px;
    font-size: 14px;
    color: #1a1a1a;
}

/* Section headers */
.section-header {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #eee;
}

/* Metric override */
[data-testid="stMetric"] {
    background: #f8f9fa;
    padding: 12px 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## 📄 Resume Job Match Scorer")
st.markdown(
    "Paste your resume and a job description below. "
    "The scorer uses **TF-IDF vectorisation + cosine similarity** to measure "
    "how well your resume matches the role, and tells you exactly what to fix."
)
st.divider()


# ── Input section ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("#### Your Resume")
    resume_input = st.text_area(
        label="resume",
        placeholder="Paste your full resume text here...",
        height=340,
        label_visibility="collapsed",
    )
    resume_len = len(resume_input.split()) if resume_input.strip() else 0
    st.caption(f"{resume_len} words")

with col_right:
    st.markdown("#### Job Description")
    job_input = st.text_area(
        label="job",
        placeholder="Paste the full job description here...",
        height=340,
        label_visibility="collapsed",
    )
    job_len = len(job_input.split()) if job_input.strip() else 0
    st.caption(f"{job_len} words")


# ── Analyse button ─────────────────────────────────────────────────────────────
st.markdown("")
btn_col, _ = st.columns([1, 3])
with btn_col:
    analyse = st.button("Analyse Match ⚡", use_container_width=True, type="primary")


# ── Results ────────────────────────────────────────────────────────────────────
if analyse:
    if not resume_input.strip() or not job_input.strip():
        st.warning("Please paste both your resume and the job description before analysing.")
        st.stop()

    if resume_len < 30:
        st.warning("Your resume looks too short. Paste the full text for accurate results.")
        st.stop()

    if job_len < 20:
        st.warning("The job description looks too short. Paste the full listing for best results.")
        st.stop()

    with st.spinner("Analysing your match..."):
        time.sleep(0.6)  # slight delay so it feels like it's working
        score = get_match_score(resume_input, job_input)
        missing = get_missing_keywords(resume_input, job_input)
        matching = get_matching_keywords(resume_input, job_input)
        label, level = get_score_label(score)
        tips = get_improvement_tips(score, missing)

    st.divider()
    st.markdown("### Your Results")
    st.markdown("")

    # ── Score circle + summary metrics ────────────────────────────────────────
    circle_class = {
        "success": "score-excellent",
        "info":    "score-good",
        "warning": "score-moderate",
        "error":   "score-low",
    }[level]

    top_left, top_mid, top_right = st.columns([1, 1, 1], gap="large")

    with top_left:
        st.markdown(
            f"""
            <div class="score-circle {circle_class}">
                {score}%
                <span style="font-size:0.9rem;font-weight:500;margin-top:4px">{label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(int(score), text="")

    with top_mid:
        st.metric("Keywords matched", len(matching))
        st.metric("Keywords missing", len(missing))

    with top_right:
        st.metric("Resume word count", resume_len)
        st.metric("JD word count", job_len)

    st.markdown("")

    # ── Keyword columns ───────────────────────────────────────────────────────
    kw_left, kw_right = st.columns(2, gap="large")

    with kw_left:
        st.markdown('<div class="section-header">✅ Keywords you already have</div>', unsafe_allow_html=True)
        if matching:
            pills_html = '<div class="pill-container">'
            for kw in matching:
                pills_html += f'<span class="pill-match">{kw}</span>'
            pills_html += "</div>"
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.info("No significant keyword overlap found.")

    with kw_right:
        st.markdown('<div class="section-header">⚠️ Keywords missing from your resume</div>', unsafe_allow_html=True)
        if missing:
            pills_html = '<div class="pill-container">'
            for kw in missing:
                pills_html += f'<span class="pill-missing">{kw}</span>'
            pills_html += "</div>"
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.success("Great — no major keywords missing!")

    st.markdown("")

    # ── Improvement tips ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">💡 How to improve your match</div>', unsafe_allow_html=True)
    tips_html = ""
    for tip in tips:
        tips_html += f'<div class="tip-card">{tip}</div>'
    st.markdown(tips_html, unsafe_allow_html=True)

    st.markdown("")

    # ── Keyword frequency chart ───────────────────────────────────────────────
    if matching:
        st.markdown('<div class="section-header">📊 Top matched keywords</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "Keyword": matching[:10],
            "In JD": [1] * min(len(matching), 10),
        }).set_index("Keyword")
        st.bar_chart(chart_data, height=220)

    st.markdown("")

    # ── Download report ───────────────────────────────────────────────────────
    report_lines = [
        "RESUME MATCH SCORE REPORT",
        "=" * 40,
        f"Match Score       : {score}%",
        f"Verdict           : {label}",
        f"Keywords matched  : {len(matching)}",
        f"Keywords missing  : {len(missing)}",
        "",
        "MATCHED KEYWORDS",
        "-" * 40,
        ", ".join(matching) if matching else "None",
        "",
        "MISSING KEYWORDS",
        "-" * 40,
        ", ".join(missing) if missing else "None",
        "",
        "IMPROVEMENT TIPS",
        "-" * 40,
    ] + [f"- {t}" for t in tips]

    report_text = "\n".join(report_lines)

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button(
            label="Download Report (.txt)",
            data=report_text,
            file_name="resume_match_report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;font-size:12px;color:#888'>"
    "Built with Python · Scikit-learn · Streamlit &nbsp;|&nbsp; "
    "<a href='https://github.com' style='color:#888'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True,
)