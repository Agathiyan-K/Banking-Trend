import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Set wide layout
st.set_page_config(layout="wide")

# Download the CSV file from Google Drive
file_url = "https://drive.google.com/uc?id=1J4SLi_lDWUuxlA-fNITtEnBwfZzIKOY2"
file_path = "bankruptcy_data.csv"
gdown.download(file_url, file_path, quiet=False)

# Load the dataset
df = pd.read_csv(file_path)

# Streamlit App Title
st.title("📊 Bankruptcy Analysis Dashboard")

# Filters
bank_types = st.multiselect("Select Bank Type", df["Bank Type"].unique())
filtered_df = df[df["Bank Type"].isin(bank_types)] if bank_types else df

companies = st.multiselect("Select Company Name", filtered_df["Company Name"].unique())
filtered_df = filtered_df[filtered_df["Company Name"].isin(companies)] if companies else filtered_df

# Create a 2x2 grid layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Plot function with legend adjustments
def create_plot(data, y_col, title, y_label):
    fig = px.line(data, x="Year", y=y_col, color="Company Name", title=title)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3))  # Move legend below
    return fig

# Generate graphs
with col1:
    st.plotly_chart(create_plot(filtered_df, "Positive Percentage", "Positive Percentage Trend", "Positive Percentage"), use_container_width=True)

with col2:
    st.plotly_chart(create_plot(filtered_df, "Negative Percentage", "Negative Percentage Trend", "Negative Percentage"), use_container_width=True)

with col3:
    st.plotly_chart(create_plot(filtered_df, "Positive Count", "Positive Count Trend", "Positive Count"), use_container_width=True)

with col4:
    st.plotly_chart(create_plot(filtered_df, "Negative Count", "Negative Count Trend", "Negative Count"), use_container_width=True)
