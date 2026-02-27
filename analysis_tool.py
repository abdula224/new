import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Data Analyzer",
    page_icon="\U0001F4CA",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("\U0001F4C2 Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "\U0001F3E0 Home",
        "\U0001F4CA Dataset Overview",
        "\U0001F4C8 Statistical Summary",
        "\U0001F525 Correlation Heatmap",
        "\U0001F3AF Column Analysis",
        "\U0001F916 ML Feasibility Check"
    ]
)

st.title("\U0001F4CA Smart Data Analyzer Dashboard")

# ---------------- HOME ----------------
if menu == "\U0001F3E0 Home":

    st.header("\U0001F4C2 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File (Max 5MB)",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        file_size = uploaded_file.size / (1024 * 1024)
        if file_size > 5:
            st.error("File size exceeds 5MB limit.")
            st.stop()

        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state["df"] = df
            st.success("File uploaded successfully.")

        except:
            st.error("Error reading file.")

# ---------------- IF DATA EXISTS ----------------
if "df" in st.session_state:

    df = st.session_state["df"]
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns

    # ---------------- DATASET OVERVIEW ----------------
    if menu == "\U0001F4CA Dataset Overview":

        st.header("Dataset Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.dataframe(df.head(), use_container_width=True)

    # ---------------- STATISTICAL SUMMARY ----------------
    elif menu == "\U0001F4C8 Statistical Summary":

        st.header("Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)

    # ---------------- CORRELATION ----------------
    elif menu == "\U0001F525 Correlation Heatmap":

        st.header("Correlation Heatmap")

        if len(numeric_cols) > 1:
            fig, ax = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Not enough numeric columns.")

    # ---------------- COLUMN ANALYSIS ----------------
    elif menu == "\U0001F3AF Column Analysis":

        st.header("Column Analysis")

        selected_column = st.selectbox("Select Column", df.columns)

        if selected_column in numeric_cols:
            st.write("Mean:", df[selected_column].mean())
            st.write("Median:", df[selected_column].median())
            st.write("Std:", df[selected_column].std())

            fig, ax = plt.subplots()
            df[selected_column].hist(ax=ax)
            st.pyplot(fig)

        else:
            value_counts = df[selected_column].value_counts()
            st.dataframe(value_counts)

    # ---------------- ML FEASIBILITY ----------------
    elif menu == "\U0001F916 ML Feasibility Check":

        st.header("\U0001F916 Machine Learning Feasibility Checker")

        ml_type = st.selectbox(
            "Select ML Type",
            ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"]
        )

        # -------- SUPERVISED --------
        if ml_type == "Supervised Learning":

            if df.shape[1] < 2:
                st.error("Dataset must contain at least 2 columns.")
            else:
                target = st.selectbox("Select Target Column", df.columns)
                feature_cols = df.columns.drop(target)

                if len(feature_cols) < 1:
                    st.error("Need at least one feature column.")
                elif df[target].nunique() == len(df[target]):
                    st.warning("Target has all unique values.")
                else:
                    st.success("Supervised Learning is POSSIBLE.")

                    if df[target].dtype == "object":
                        st.info("Problem Type: Classification")
                    else:
                        st.info("Problem Type: Regression")

        # -------- UNSUPERVISED --------
        elif ml_type == "Unsupervised Learning":

            if len(numeric_cols) < 2:
                st.error("Need at least 2 numeric columns.")
            else:
                st.success("Unsupervised Learning is POSSIBLE.")
                st.info("Recommended: Clustering")

        # -------- REINFORCEMENT --------
        elif ml_type == "Reinforcement Learning":

            st.warning("Requires environment + reward system.")
            st.error("Static CSV dataset not suitable.")

# ---------------- IF DATA NOT UPLOADED ----------------
else:
    if menu != "\U0001F3E0 Home":
        st.warning("Please upload a dataset from Home section first.")