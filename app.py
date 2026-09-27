import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------
# Import Project Modules
# --------------------------

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

# --------------------------
# Page Configuration
# --------------------------

st.set_page_config(
    page_title="CleanAI",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# Session State
# --------------------------

if "df" not in st.session_state:
    st.session_state.df = None

# --------------------------
# Sidebar
# --------------------------

with st.sidebar:

    st.title("🧹 CleanAI")
    st.caption("LLM-Powered Data Cleaning Assistant")

    st.markdown("---")

    st.write("## Development Progress")

    st.progress(4/6)

    st.caption("Module 4 of 6 Completed")

    st.write("✅ Project Setup")
    st.write("✅ Smart Data Loader")
    st.write("✅ Automated Data Profiler")
    st.write("✅ Intelligent Issue Detection")
    st.write("⬜️ LLM Recommendations")
    st.write("⬜️ Auto Cleaning Engine")

# --------------------------
# Main Header
# --------------------------

st.title("🧹 CleanAI")

st.subheader("LLM-Powered Data Cleaning Assistant")

st.write(
    """
    Upload a messy CSV file and automatically:

    - 📂 Import datasets safely
    - 📊 Generate a data profile
    - 🚨 Detect data quality issues
    - 📈 Visualize dataset health
    - 🤖 Prepare AI-powered cleaning recommendations
    """
)

# --------------------------
# File Upload
# --------------------------

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

skip_bad_rows = st.checkbox(
    "Skip corrupted rows during import"
)

# --------------------------
# File Processing
# --------------------------

if uploaded_file:

    with st.spinner("Importing dataset..."):

        df, encoding, error = load_csv(
            uploaded_file,
            skip_bad_rows=skip_bad_rows
        )

    if error:

        st.error(error)

    else:

        st.session_state.df = df

        info = get_file_info(uploaded_file, df)

        summary = create_import_summary(df)

        # ==========================================================
        # IMPORT SUCCESS
        # ==========================================================

        st.success("Dataset imported successfully!")

        st.info(f"Detected Encoding: {encoding}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", f"{info['rows']:,}")
        col2.metric("Columns", info["columns"])
        col3.metric("File Size", f"{info['size_mb']} MB")
        col4.metric("Memory", f"{info['memory_mb']} MB")

        # ==========================================================
        # IMPORT SUMMARY
        # ==========================================================

        st.divider()

        st.header("📋 Import Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Missing Cells", summary["missing_cells"])
        c2.metric("Duplicate Rows", summary["duplicate_rows"])
        c3.metric(
            "Numeric Columns",
            len(df.select_dtypes(include="number").columns)
        )
        c4.metric(
            "Text Columns",
            len(df.select_dtypes(include="object").columns)
        )

        # ==========================================================
        # BASIC DATA PREVIEW
        # ==========================================================

        with st.expander("📄 Dataset Preview", expanded=True):

            st.dataframe(
                df.head(20),
                use_container_width=True
            )

        with st.expander("📋 Column Information"):

            column_info = pd.DataFrame({
                "Column": df.columns,

                "Data Type": df.dtypes.astype(str),

                "Missing": df.isnull().sum(),

                "Unique": df.nunique()

            })

            st.dataframe(
                column_info,
                use_container_width=True
            )

        with st.expander("🔢 Missing Value Analysis"):

            missing_df = missing_summary(df)

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        # ==========================================================
        # MODULE 3 — DATA PROFILER
        # ==========================================================

        st.divider()

        st.header("📊 Automated Data Profiler")

        profile = generate_profile(df)

        quality_score = calculate_quality_score(df)

        # --------------------------
        # Quality Score Gauge
        # --------------------------

        gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=quality_score,

            title={"text": "Data Quality Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "royalblue"}

            }

        ))

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # --------------------------
        # Overview Cards
        # --------------------------

        p1, p2, p3, p4 = st.columns(4)

        p1.metric("Rows", profile["rows"])
        p2.metric("Columns", profile["columns"])
        p3.metric("Duplicates", profile["duplicate_rows"])
        p4.metric("Missing Cells", profile["missing_cells"])

        # --------------------------
        # Missing Values Chart
        # --------------------------

        st.subheader("Missing Values by Column")

        fig = px.bar(

            missing_df,

            x="Column",

            y="Missing",

            title="Missing Values"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # --------------------------
        # Data Type Distribution
        # --------------------------

        st.subheader("Data Type Distribution")

        dtype_counts = df.dtypes.astype(str).value_counts()

        fig = px.pie(

            names=dtype_counts.index,

            values=dtype_counts.values,

            title="Column Data Types"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # --------------------------
        # Outlier Detection
        # --------------------------

        st.subheader("Outlier Detection")

        outlier_df = detect_outliers(df)

        fig = px.bar(

            outlier_df,

            x="Column",

            y="Outliers",

            title="Detected Outliers (IQR Method)"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # --------------------------
        # Detailed Reports
        # --------------------------

        with st.expander("📋 Column Health Report"):

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

        # ==========================================================
        # MODULE 4 — ISSUE DETECTION ENGINE
        # ==========================================================

        st.divider()

        st.header("🚨 Intelligent Issue Detection")

        issues_df = detect_all_issues(df)

        if issues_df.empty:

            st.success("No issues detected.")

        else:

            high = (issues_df["Severity"] == "High").sum()
            medium = (issues_df["Severity"] == "Medium").sum()
            low = (issues_df["Severity"] == "Low").sum()

            h1, h2, h3 = st.columns(3)

            h1.metric("🔴 High", high)
            h2.metric("🟡 Medium", medium)
            h3.metric("🔵 Low", low)

            st.subheader("Detected Issues")

            st.dataframe(
                issues_df,
                use_container_width=True
            )

            # --------------------------
            # Severity Distribution
            # --------------------------

            st.subheader("Issue Severity Distribution")

            severity_counts = issues_df["Severity"].value_counts()

            fig = px.bar(

                x=severity_counts.index,

                y=severity_counts.values,

                labels={

                    "x": "Severity",

                    "y": "Issues"

                },

                title="Issue Severity"

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # --------------------------
            # Priority Recommendations
            # --------------------------

            st.subheader("Priority Recommendations")

            if high > 0:
                st.error(
                    f"Resolve {high} High Priority issue(s) first."
                )

            if medium > 0:
                st.warning(
                    f"Review {medium} Medium Priority issue(s)."
                )

            if low > 0:
                st.info(
                    f"Improve {low} Low Priority consistency issue(s)."
                )

        # ==========================================================
        # NEXT MODULE PREVIEW
        # ==========================================================

        st.divider()

        st.header("🤖 Coming Next")

        st.info(
            """
            Module 5 Preview

            Soon CleanAI will use the Gemini API to:

            - Generate AI-powered cleaning recommendations
            - Assign confidence scores
            - Estimate cleaning risks
            - Produce a structured JSON cleaning plan
            - Explain why each cleaning action is recommended
            """
        )
