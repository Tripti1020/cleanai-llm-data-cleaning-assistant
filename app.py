import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import (
    load_csv,
    get_file_info,
    create_import_summary,
)

from src.profiler import (
    generate_profile,
    column_health,
    numeric_summary,
    categorical_summary,
    missing_summary,
    detect_outliers,
)

from src.quality_score import calculate_quality_score


# --------------------------
# Page Configuration
# --------------------------

st.set_page_config(
    page_title="CleanAI",
    page_icon="🧹",
    layout="wide",
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

    st.progress(2.5 / 6)
    st.caption("Module 2.5 of 6")

    st.write("✅ Project Setup")
    st.write("✅ Smart Data Loader")
    st.write("🟡 Production Import")
    st.write("⬜ Data Profiling")
    st.write("⬜ AI Recommendations")


# --------------------------
# Main Page
# --------------------------

st.title("🧹 CleanAI")
st.subheader("Production-Grade CSV Import")

st.write(
    "Upload messy CSV files with automatic encoding detection and safe import."
)

uploaded_file = st.file_uploader(
    "Drag & Drop CSV",
    type=["csv"],
)

skip_bad_rows = st.checkbox(
    "Skip corrupted rows during import",
)


# --------------------------
# Import Logic
# --------------------------

if uploaded_file:
    with st.spinner("Importing dataset..."):
        df, encoding, error = load_csv(
            uploaded_file,
            skip_bad_rows=skip_bad_rows,
        )

    if error:
        st.error(error)

    else:
        st.session_state.df = df

        info = get_file_info(uploaded_file, df)
        summary = create_import_summary(df)

        st.success("Dataset imported successfully!")

        # --------------------------
        # Import Summary
        # --------------------------

        st.info(f"**Detected Encoding:** `{encoding}`")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", f"{info['rows']:,}")
        col2.metric("Columns", info["columns"])
        col3.metric("File Size", f"{info['size_mb']} MB")
        col4.metric("Memory", f"{info['memory_mb']} MB")

        # --------------------------
        # Dataset Health
        # --------------------------

        st.divider()

        st.write("## Import Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Missing Cells",
            summary["missing_cells"],
        )

        c2.metric(
            "Duplicate Rows",
            summary["duplicate_rows"],
        )

        c3.metric(
            "Numeric Columns",
            len(df.select_dtypes(include="number").columns),
        )

        c4.metric(
            "Text Columns",
            len(df.select_dtypes(include="object").columns),
        )

        # --------------------------
        # Preview
        # --------------------------

        with st.expander("📄 Dataset Preview", expanded=True):
            st.dataframe(
                df.head(20),
                use_container_width=True,
            )

        # --------------------------
        # Column Information
        # --------------------------

        with st.expander("📋 Column Information"):
            column_info = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str),
                    "Missing": df.isnull().sum(),
                    "Unique": df.nunique(),
                }
            )

            st.dataframe(
                column_info,
                use_container_width=True,
            )

        # --------------------------
        # Missing Values
        # --------------------------

        with st.expander("🔢 Missing Value Analysis"):
            missing_df = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Missing": df.isnull().sum(),
                    "Percentage": (
                        df.isnull().sum() / len(df) * 100
                    ).round(2),
                }
            )

            st.dataframe(
                missing_df,
                use_container_width=True,
            )

        # --------------------------
        # Data Profiler
        # --------------------------

        st.divider()

        st.title("📊 Automated Data Profiler")

        profile = generate_profile(df)
        quality_score = calculate_quality_score(df)

        # --------------------------
        # Quality Gauge
        # --------------------------

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=quality_score,
                title={"text": "Data Quality Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "royalblue"},
                },
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # --------------------------
        # Overview Cards
        # --------------------------

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Rows",
            profile["rows"],
        )

        c2.metric(
            "Columns",
            profile["columns"],
        )

        c3.metric(
            "Duplicates",
            profile["duplicate_rows"],
        )

        c4.metric(
            "Missing Cells",
            profile["missing_cells"],
        )

        # --------------------------
        # Missing Value Chart
        # --------------------------

        st.subheader("Missing Values by Column")

        missing_df = missing_summary(df)

        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing",
            title="Missing Values",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # --------------------------
        # Data Type Distribution
        # --------------------------

        st.subheader("Data Type Distribution")

        dtype_counts = df.dtypes.astype(str).value_counts()

        fig = px.pie(
            names=dtype_counts.index,
            values=dtype_counts.values,
            title="Column Data Types",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # --------------------------
        # Outlier Chart
        # --------------------------

        st.subheader("Outlier Detection")

        outlier_df = detect_outliers(df)

        fig = px.bar(
            outlier_df,
            x="Column",
            y="Outliers",
            title="Detected Outliers (IQR)",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # --------------------------
        # Expandable Reports
        # --------------------------

        with st.expander("📋 Column Health Report"):
            st.dataframe(
                column_health(df),
                use_container_width=True,
            )

        with st.expander("📈 Numeric Statistics"):
            st.dataframe(
                numeric_summary(df),
                use_container_width=True,
            )

        with st.expander("🔤 Categorical Summary"):
            st.dataframe(
                categorical_summary(df),
                use_container_width=True,
            )