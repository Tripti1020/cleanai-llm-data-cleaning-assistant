import streamlit as st
import pandas as pd

from src.data_loader import load_csv, get_file_info

# --------------------------
# PAGE CONFIGURATION
# --------------------------

st.set_page_config(
    page_title="CleanAI",
    page_icon="🧹",
    layout="wide"
)

# --------------------------
# SESSION STATE
# --------------------------

if "df" not in st.session_state:
    st.session_state.df = None

# --------------------------
# SIDEBAR
# --------------------------

with st.sidebar:

    st.title("🧹 CleanAI")
    st.caption("LLM-Powered Data Cleaning Assistant")

    st.markdown("---")

    st.write("## Development Progress")

    st.progress(2/6)

    st.caption("Module 2 of 6 Completed")

    st.write("✅ Project Setup")
    st.write("✅ Data Loader")
    st.write("⬜ Data Profiling")
    st.write("⬜ Issue Detection")
    st.write("⬜ AI Recommendations")

# --------------------------
# MAIN PAGE
# --------------------------

st.title("🧹 CleanAI")

st.subheader("Upload a Messy CSV Dataset")

uploaded_file = st.file_uploader(
    "Drag & Drop or Browse",
    type=["csv"]
)

# --------------------------
# FILE PROCESSING
# --------------------------

if uploaded_file:

    df, error = load_csv(uploaded_file)

    if error:

        st.error(error)

    else:

        st.session_state.df = df

        info = get_file_info(uploaded_file, df)

        st.success("Dataset loaded successfully!")

        # --------------------------
        # FILE METRICS
        # --------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", f"{info['rows']:,}")
        col2.metric("Columns", info["columns"])
        col3.metric("File Size", f"{info['size_mb']} MB")
        col4.metric("Memory", f"{info['memory_mb']} MB")

        # --------------------------
        # QUICK HEALTH
        # --------------------------

        st.divider()

        st.write("## Quick Dataset Health")

        duplicates = df.duplicated().sum()
        missing = df.isnull().sum().sum()
        numeric_cols = len(df.select_dtypes(include="number").columns)
        text_cols = len(df.select_dtypes(include="object").columns)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Missing Cells", missing)
        c2.metric("Duplicate Rows", duplicates)
        c3.metric("Numeric Columns", numeric_cols)
        c4.metric("Text Columns", text_cols)

        # --------------------------
        # COLUMN INFO TABLE
        # --------------------------

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        # --------------------------
        # EXPANDABLE SECTIONS
        # --------------------------

        with st.expander("📄 Dataset Preview", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)

        with st.expander("📋 Column Information"):
            st.dataframe(column_info, use_container_width=True)

        with st.expander("🔢 Missing Values Summary"):

            missing_df = pd.DataFrame({
                "Column": df.columns,
                "Missing": df.isnull().sum().values,
                "Percentage": (
                    df.isnull().sum()/len(df)*100
                ).round(2).values
            })

            st.dataframe(missing_df, use_container_width=True)