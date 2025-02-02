import pandas as pd
import plotly.express as px
import streamlit as st
import gdown

# Download the CSV file from Google Drive
file_url = "https://drive.google.com/uc?id=1J4SLi_lDWUuxlA-fNITtEnBwfZzIKOY2"
file_path = "bankruptcy_data.csv"
gdown.download(file_url, file_path, quiet=False)

# Load the dataset
df = pd.read_csv(file_path)

# Streamlit App Title
st.title("📊 Bankruptcy Analysis Dashboard")

# Multi-select dropdowns
bank_types = st.multiselect("Select Bank Type(s):", df["Bank Type"].unique())

# Filter company names based on selected bank types
if bank_types:
    filtered_df = df[df["Bank Type"].isin(bank_types)]
    company_names = st.multiselect("Select Company Name(s):", filtered_df["Company Name"].unique())
else:
    company_names = []

# Filter data based on selections
if bank_types and company_names:
    filtered_df = df[(df["Bank Type"].isin(bank_types)) & (df["Company Name"].isin(company_names))]

    # Create trend graphs
    fig1 = px.line(filtered_df, x="Year", y="Positive Percentage", color="Company Name", title="Positive Percentage Trend")
    fig2 = px.line(filtered_df, x="Year", y="Negative Percentage", color="Company Name", title="Negative Percentage Trend")
    fig3 = px.line(filtered_df, x="Year", y="Positive Count", color="Company Name", title="Positive Count Trend")
    fig4 = px.line(filtered_df, x="Year", y="Negative Count", color="Company Name", title="Negative Count Trend")

    # Display graphs in a 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("⚠️ Please select at least one Bank Type and one Company Name to view the trends.")

# Run using: streamlit run app.py
