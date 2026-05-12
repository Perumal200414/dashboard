import streamlit as st
import pandas as pd
import numpy as np

# Safe import handling
try:
    from sklearn.preprocessing import LabelEncoder
except ImportError:
    st.error("Scikit-learn is not installed.")
    st.info("Install it using: pip install scikit-learn")
    st.stop()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Workforce Attrition Analysis",
    layout="wide"
)

st.title("Workforce Attrition Patterns and Risk Hotspot Analysis")
st.write("Employee Attrition Dashboard using Streamlit")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload Employee CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Load data
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -------------------------------
    # BASIC INFO
    # -------------------------------
    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        missing = df.isnull().sum().sum()
        st.metric("Missing Values", missing)

    # -------------------------------
    # HANDLE CATEGORICAL DATA
    # -------------------------------
    st.subheader("Encoding Categorical Columns")

    encoder = LabelEncoder()

    categorical_cols = df.select_dtypes(include=["object"]).columns

    encoded_df = df.copy()

    for col in categorical_cols:
        encoded_df[col] = encoder.fit_transform(
            encoded_df[col].astype(str)
        )

    st.success("Categorical columns encoded successfully")

    st.subheader("Encoded Dataset Preview")
    st.dataframe(encoded_df.head())

    # -------------------------------
    # ATTRITION ANALYSIS
    # -------------------------------
    if "Attrition" in df.columns:

        st.subheader("Attrition Analysis")

        attrition_counts = df["Attrition"].value_counts()

        st.bar_chart(attrition_counts)

        attrition_rate = (
            attrition_counts.get("Yes", 0)
            / len(df)
        ) * 100

        st.metric(
            "Attrition Rate",
            f"{attrition_rate:.2f}%"
        )

    else:
        st.warning(
            "Column 'Attrition' not found in dataset."
        )

else:
    st.info("Please upload a CSV dataset to continue.")