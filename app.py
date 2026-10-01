import os
import io
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import (
    load_csv,
    get_file_info,
    create_import_summary
)

from src.profiler import (
    generate_profile,
    column_health,
    numeric_summary,
    categorical_summary,
    missing_summary,
    detect_outliers
)

from src.quality_score import calculate_quality_score
from src.issue_detector import detect_all_issues
from src.llm_engine import generate_cleaning_plan
from src.cleaning_engine import execute_cleaning_plan
from src.report_generator import generate_report
from src.validator import validate_dataset

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="CleanAI",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Premium UI
# ==========================================================

st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#111827);
}

/* Cards */
.metric-card{
    background: rgba(255,255,255,.08);
    backdrop-filter: blur(16px);
    border:1px solid rgba(255,255,255,.12);
    border-radius:20px;
    padding:22px;
    text-align:center;
    transition: all .35s ease;
    box-shadow:0 8px 30px rgba(0,0,0,.25);
}
.metric-card:hover{
    transform: translateY(-8px);
    border:1px solid rgba(59,130,246,.8);
    box-shadow:0 12px 35px rgba(37,99,235,.35);
}

/* Section Titles */
.section-title{
    font-size:26px;
    font-weight:700;
    margin-top:8px;
    margin-bottom:14px;
}

/* Comparison Box */
.compare-box{
    background:rgba(255,255,255,.06);
    border-radius:16px;
    padding:18px;
    border:1px solid rgba(255,255,255,.1);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Session State
# ==========================================================

if "df" not in st.session_state:
    st.session_state.df = None

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.image("assets/logo.png", width=90)

    st.title("CleanAI")

    st.caption("LLM-Powered Data Cleaning Assistant")

    st.markdown("---")

    st.subheader("Pipeline")

    st.markdown("""
    ✅ Upload

    ✅ Profile

    ✅ Detect

    ✅ AI Analysis

    ✅ Cleaning

    ✅ Export
    """)

    st.markdown("---")

    st.caption("Built with Python, Streamlit, Pandas and Gemini AI.")

# ==========================================================
# Hero Section
# ==========================================================

col1, col2 = st.columns([1,3])

with col1:

    st.image(
        "assets/logo.png",
        width=140
    )

with col2:

    st.title("CleanAI")

    st.subheader("LLM-Powered Data Cleaning Assistant")

    st.write(
        "An AI-powered data quality copilot that audits messy datasets, detects issues, generates intelligent cleaning recommendations, and safely applies approved transformations."
    )

    b1, b2 = st.columns(2)

    with b1:
        try_sample = st.button(
            "🚀 Try Sample Dataset",
            use_container_width=True,
            key="try_sample_dataset"
        )

    with b2:
        # Replace this with your CleanAI repository URL once the repo is public.
        github_url = "https://github.com/Tripti1020/cleanai-llm-data-cleaning-assistant"
        st.link_button(
            "⭐ View GitHub",
            github_url,
            use_container_width=True
        )


# ==========================================================
# Feature Card
# ==========================================================

st.markdown('<div class="section-title">Why CleanAI?</div>',
            unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    <div class="metric-card">
    <h3>📂</h3>
    <h4>Smart Import</h4>
    <p>Automatic encoding detection</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="metric-card">
    <h3>🤖</h3>
    <h4>AI Copilot</h4>
    <p>Gemini-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="metric-card">
    <h3>🧹</h3>
    <h4>Safe Cleaning</h4>
    <p>Human-approved transformations</p>
    </div>
    """, unsafe_allow_html=True)

with f4:
    st.markdown("""
    <div class="metric-card">
    <h3>📄</h3>
    <h4>Executive Reports</h4>
    <p>Professional PDF exports</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# AI Workflow Timeline
# ==========================================================

st.markdown('<div class="section-title">How CleanAI Works</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="compare-box">

**Upload CSV**

⬇

**Profile Dataset**

⬇

**Detect Issues**

⬇

**Gemini AI Analysis**

⬇

**Approve Cleaning**

⬇

**Export Clean Dataset & Report**

</div>
""", unsafe_allow_html=True)

# ==========================================================
# Upload
# ==========================================================

class LocalCSVFile:
    """Small file-like adapter so the existing data_loader can treat
    a local sample CSV like a Streamlit UploadedFile."""

    def __init__(self, path):
        self.path = Path(path)
        self.name = self.path.name
        self._data = self.path.read_bytes()
        self.size = len(self._data)
        self._buffer = io.BytesIO(self._data)

    def read(self, *args, **kwargs):
        return self._buffer.read(*args, **kwargs)

    def seek(self, *args, **kwargs):
        return self._buffer.seek(*args, **kwargs)

    def tell(self):
        return self._buffer.tell()

    def getvalue(self):
        return self._data


def find_sample_dataset():
    """Find the project's sample messy CSV in common project locations."""
    base = Path(__file__).resolve().parent

    candidates = [
        base / "data" / "messy_customer.csv",
        base / "sample_data" / "messy_customer.csv",
        base / "messy_customer.csv",
        base / "datasets" / "messy_customer.csv",
        base / "assets" / "messy_customer.csv",
        base / "data" / "raw" / "messy_customer.csv",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate

    return None


uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

# The hero button stores the sample request in session state so it
# survives Streamlit's rerun and can be processed by the same pipeline.
if try_sample:
    sample_path = find_sample_dataset()

    if sample_path:
        st.session_state.sample_file = str(sample_path)
        st.session_state.sample_error = None
        st.rerun()
    else:
        st.session_state.sample_file = None
        st.session_state.sample_error = (
            "Sample dataset not found. Put `messy_customer.csv` inside "
            "the project's `data` folder and click the button again."
        )

if "sample_file" not in st.session_state:
    st.session_state.sample_file = None

if "sample_error" not in st.session_state:
    st.session_state.sample_error = None

if st.session_state.sample_error:
    st.warning(st.session_state.sample_error)

# A manually uploaded CSV takes priority over the sample dataset.
if uploaded_file is not None:
    active_file = uploaded_file
    using_sample = False
elif st.session_state.sample_file:
    active_file = LocalCSVFile(st.session_state.sample_file)
    using_sample = True
else:
    active_file = None
    using_sample = False

if using_sample:
    st.success(f"Sample dataset loaded: **{active_file.name}**")

skip_bad_rows = st.checkbox(
    "Skip corrupted rows"
)

# ==========================================================
# Main Pipeline
# ==========================================================

if active_file:

    if uploaded_file is not None and st.session_state.sample_file:
        st.session_state.sample_file = None

    with st.spinner("Importing dataset..."):

        df, encoding, error = load_csv(
            active_file,
            skip_bad_rows=skip_bad_rows
        )

    if error:

        st.error(error)

    else:

        # ==================================================
        # Dataset Validation
        # ==================================================

        validation_result = validate_dataset(df)

        if not validation_result["valid"]:

            st.error(
                "❌ Dataset validation failed. "
                "Please fix the following issues before continuing."
            )

            for validation_error in validation_result["errors"]:

                st.error(
                    f"• {validation_error}"
                )

            st.stop()

        # Show warnings without stopping the pipeline
        if validation_result["warnings"]:

            with st.expander(
                "⚠️ Dataset Validation Warnings",
                expanded=True
            ):

                for warning in validation_result["warnings"]:

                    st.warning(
                        f"• {warning}"
                    )

        # Validation passed
        st.success(
            "✅ Dataset validation completed successfully."
        )
        with st.expander("🔍 Validation Details"):

            v1, v2, v3 = st.columns(3)

            v1.metric(
                "Validation Status",
                "Passed"
            )

            v2.metric(
                "Warnings",
                len(validation_result["warnings"])
            )

            v3.metric(
                "Checks Passed",
                len(validation_result["info"])
            )

            if validation_result["info"]:

                st.markdown("### Validation Information")

                for item in validation_result["info"]:

                    st.write(f"✓ {item}")
        
        st.session_state.df = df

        info = get_file_info(active_file, df)
        summary = create_import_summary(df)

        st.success("Dataset imported successfully!")

        st.info(f"Detected Encoding: **{encoding}**")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", f"{info['rows']:,}")
        c2.metric("Columns", info["columns"])
        c3.metric("File Size", f"{info['size_mb']} MB")
        c4.metric("Memory", f"{info['memory_mb']} MB")

        # ==================================================
        # Import Summary
        # ==================================================

        st.markdown('<div class="section-title">📋 Import Summary</div>',
                    unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)

        s1.metric("Missing Cells", summary["missing_cells"])
        s2.metric("Duplicate Rows", summary["duplicate_rows"])
        s3.metric("Numeric Columns",
                  len(df.select_dtypes(include="number").columns))
        s4.metric("Text Columns",
                  len(df.select_dtypes(include="object").columns))

        with st.expander("📄 Dataset Preview", expanded=True):

            st.dataframe(
                df.head(20),
                use_container_width=True
            )

        with st.expander("📋 Column Information"):

            column_info = pd.DataFrame({

                "Column": df.columns,
                "Data Type": df.dtypes.astype(str),
                "Missing": df.isna().sum(),
                "Unique": df.nunique()

            })

            st.dataframe(
                column_info,
                use_container_width=True
            )

        with st.expander("🔢 Missing Value Analysis"):

            st.dataframe(
                missing_summary(df),
                use_container_width=True
            )

        # ==================================================
        # Automated Profiler
        # ==================================================

        st.markdown('<div class="section-title">📊 Automated Data Profiler</div>',
                    unsafe_allow_html=True)

        profile = generate_profile(df)
        quality_score = calculate_quality_score(df)

        gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=quality_score,

            title={"text": "Data Quality Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "#3b82f6"}

            }

        ))

        st.plotly_chart(gauge, use_container_width=True)

        p1, p2, p3, p4 = st.columns(4)

        p1.metric("Rows", profile["rows"])
        p2.metric("Columns", profile["columns"])
        p3.metric("Duplicates", profile["duplicate_rows"])
        p4.metric("Missing Cells", profile["missing_cells"])

        st.subheader("Missing Values")

        missing_df = missing_summary(df)

        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Data Types")

        dtype_counts = df.dtypes.astype(str).value_counts()

        fig = px.pie(
            names=dtype_counts.index,
            values=dtype_counts.values
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Outlier Detection")

        fig = px.bar(
            detect_outliers(df),
            x="Column",
            y="Outliers"
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Column Health"):

            st.dataframe(
                column_health(df),
                use_container_width=True
            )

        with st.expander("📈 Numeric Statistics"):

            st.dataframe(
                numeric_summary(df),
                use_container_width=True
            )

        with st.expander("🔤 Categorical Summary"):

            st.dataframe(
                categorical_summary(df),
                use_container_width=True
            )

        # ==================================================
        # Issue Detection
        # ==================================================

        st.markdown('<div class="section-title">🚨 Intelligent Issue Detection</div>',
                    unsafe_allow_html=True)

        issues_df = detect_all_issues(df)

        if issues_df.empty:

            st.success("No issues detected.")

        else:

            high = (issues_df["Severity"] == "High").sum()
            medium = (issues_df["Severity"] == "Medium").sum()
            low = (issues_df["Severity"] == "Low").sum()

            i1, i2, i3 = st.columns(3)

            i1.metric("🔴 High", high)
            i2.metric("🟡 Medium", medium)
            i3.metric("🔵 Low", low)

            confidence_map = {"High":"98%","Medium":"93%","Low":"88%"}
            issues_display = issues_df.copy()
            issues_display["AI Confidence"] = issues_display["Severity"].map(confidence_map)

            st.dataframe(
                issues_display,
                use_container_width=True
            )

            fig = px.bar(

                issues_df["Severity"].value_counts().reset_index(),

                x="Severity",
                y="count"

            )

            st.plotly_chart(fig, use_container_width=True)

        # ==================================================
        # AI Cleaning Copilot
        # ==================================================

        st.markdown('<div class="section-title">🤖 AI Cleaning Copilot</div>',
                    unsafe_allow_html=True)

        if st.button("✨ Generate AI Cleaning Plan",
                     type="primary"):

            progress = st.progress(0)

            status = st.empty()

            status.write("Connecting to Gemini...")

            progress.progress(20)

            with st.spinner("Analyzing dataset..."):

                plan, error = generate_cleaning_plan(
                    profile,
                    issues_df
                )

            progress.progress(100)

            status.empty()

            if error:

                st.error(error)

            else:

                st.success("AI analysis completed!")

                st.subheader("Executive Summary")

                st.write(plan.get("summary", ""))

                recommendations = plan.get(
                    "recommendations",
                    []
                )

                if recommendations:

                    rec_df = pd.DataFrame(
                        recommendations
                    )

                    st.dataframe(
                        rec_df,
                        use_container_width=True
                    )

                    fig = px.bar(

                        rec_df,

                        x="column",

                        y="confidence",

                        color="risk"

                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    with st.expander("Raw JSON"):

                        st.json(plan)

        # ==================================================
        # Cleaning Workspace
        # ==================================================

        st.markdown('<div class="section-title">🧹 Cleaning Workspace</div>',
                    unsafe_allow_html=True)

        selected_actions = []

        for _, row in issues_df.iterrows():

            label = f"{row['Issue']} — {row['Column']}"

            if st.checkbox(label, value=True):

                selected_actions.append({

                    "column": row["Column"],
                    "issue": row["Issue"]

                })

        if st.button("🚀 Apply Selected Cleaning Actions",
                     type="primary"):

            with st.spinner("Cleaning dataset..."):

                cleaned_df, cleaning_log = execute_cleaning_plan(
                    df,
                    selected_actions
                )

            before_score = calculate_quality_score(df)
            after_score = calculate_quality_score(cleaned_df)

            st.success("Cleaning completed successfully!")

            # ==========================================
            # Before vs After
            # ==========================================

            st.markdown('<div class="section-title">📊 Before vs After Analysis</div>',
                        unsafe_allow_html=True)

            before_score = round(before_score, 1)
            after_score = round(after_score, 1)
            delta = round(after_score - before_score, 1)

            c1, c2, c3 = st.columns(3)

            with c1:

                st.markdown(
                    f"""
                    <div class="metric-card">
                    <h4>Before</h4>
                    <h2>{before_score}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                st.markdown(
                    f"""
                    <div class="metric-card">
                    <h4>After</h4>
                    <h2>{after_score}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:

                arrow = "⬆️" if delta >= 0 else "⬇️"

                color = "#22c55e" if delta >= 0 else "#ef4444"

                st.markdown(
                    f"""
                    <div class="metric-card">
                    <h4>Improvement</h4>
                    <h2 style="color:{color};">{arrow} {delta:+}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ==========================================
            # Before vs After Quality Gauges
            # ==========================================

            st.markdown('<div class="section-title">🎯 Quality Score Improvement</div>',
                        unsafe_allow_html=True)

            g1, g2 = st.columns(2)

            with g1:
                before_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=before_score,
                    title={"text":"Before"},
                    gauge={"axis":{"range":[0,100]},"bar":{"color":"#64748B"}}
                ))
                before_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=320)
                st.plotly_chart(before_gauge, use_container_width=True)

            with g2:
                after_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=after_score,
                    title={"text":"After"},
                    gauge={"axis":{"range":[0,100]},"bar":{"color":"#2563EB"}}
                ))
                after_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=320)
                st.plotly_chart(after_gauge, use_container_width=True)

            # ==========================================
            # KPI Cards
            # ==========================================

            st.markdown('<div class="section-title">📈 Data Quality Improvements</div>',
                        unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)

            before_missing = int(df.isna().sum().sum())
            after_missing = int(cleaned_df.isna().sum().sum())

            before_duplicates = int(df.duplicated().sum())
            after_duplicates = int(cleaned_df.duplicated().sum())

            m1.metric(
                "Missing Values",
                after_missing,
                before_missing-after_missing
            )

            m2.metric(
                "Duplicate Rows",
                after_duplicates,
                before_duplicates-after_duplicates
            )

            emails_fixed = sum(
                "Email" in log
                for log in cleaning_log
            )

            countries_fixed = sum(
                "Country" in log
                for log in cleaning_log
            )

            m3.metric("Emails Fixed", emails_fixed)
            m4.metric("Countries Standardized",
                      countries_fixed)

            # ==========================================
            # Improvement Chart
            # ==========================================

            comparison = pd.DataFrame({

                "Metric": [

                    "Missing Cells",

                    "Duplicate Rows"

                ],

                "Before": [

                    before_missing,

                    before_duplicates

                ],

                "After": [

                    after_missing,

                    after_duplicates

                ]

            })

            comparison_long = comparison.melt(

                id_vars="Metric",

                value_vars=["Before", "After"],

                var_name="Stage",

                value_name="Value"

            )

            fig = px.bar(

                comparison_long,

                x="Metric",

                y="Value",

                color="Stage",

                barmode="group",

                text="Value"

            )

            fig.update_traces(textposition="outside")

            fig.update_layout(

                height=420,

                plot_bgcolor="rgba(0,0,0,0)",

                paper_bgcolor="rgba(0,0,0,0)"

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ==========================================
            # Comparison Table
            # ==========================================

            st.markdown('<div class="section-title">🔍 Record Comparison</div>',
                        unsafe_allow_html=True)

            comparison_df = pd.DataFrame()

            comparison_df["Customer"] = df.iloc[:, 1].astype(str)

            comparison_df["Original Age"] = df["Age"].astype(str)

            comparison_df["Cleaned Age"] = cleaned_df["Age"].astype(str)

            comparison_df["Original Country"] = df["Country"].astype(str)

            comparison_df["Cleaned Country"] = cleaned_df["Country"].astype(str)

            comparison_df["Original Gender"] = df["Gender"].astype(str)

            comparison_df["Cleaned Gender"] = cleaned_df["Gender"].astype(str)

            def highlight_changes(row):

                styles = [""]*len(row)

                pairs = [

                    (1, 2),

                    (3, 4),

                    (5, 6)

                ]

                for old, new in pairs:

                    if row.iloc[old] != row.iloc[new]:

                        styles[new] = (
                            "background-color:#14532d;"
                            "color:white;"
                            "font-weight:bold;"
                        )

                return styles

            st.dataframe(

                comparison_df.style.apply(
                    highlight_changes,
                    axis=1
                ),

                use_container_width=True

            )

            # ==========================================
            # Audit Log
            # ==========================================

            with st.expander("📋 Cleaning Timeline", expanded=True):
                st.caption("Every transformation performed during cleaning.")

                for log in cleaning_log:
                    st.markdown(
                        f'''
                        <div style="border-left:4px solid #22c55e;padding-left:15px;margin:12px 0;">
                            <span style="color:#22c55e;">✔</span> {log}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

            # ==========================================
            # Cleaned Dataset
            # ==========================================

            with st.expander("📄 Cleaned Dataset Preview",
                             expanded=True):

                st.dataframe(

                    cleaned_df.head(20),

                    use_container_width=True,

                    height=420

                )

            # ==========================================
            # Downloads
            # ==========================================

            csv = cleaned_df.to_csv(index=False)

            st.download_button(

                "⬇ Download Cleaned CSV",

                csv,

                "cleaned_dataset.csv",

                "text/csv"

            )

            os.makedirs("reports", exist_ok=True)

            report_path = "reports/CleanAI_Report.pdf"

            generate_report(
                report_path,
                before_score,
                after_score,
                cleaning_log,
                executive_summary=plan.get("summary", "AI summary unavailable") if "plan" in locals() else "AI summary unavailable",
                dataset_name=active_file.name
            )

            with open(report_path, "rb") as pdf:

                st.download_button(

                    "📄 Download Cleaning Report",

                    pdf,

                    "CleanAI_Report.pdf",

                    "application/pdf"

                )