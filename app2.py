import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Set wide layout
st.set_page_config(layout="wide")

# Google Drive File URL
drive_url = "https://drive.google.com/uc?id=1J4SLi_lDWUuxlA-fNITtEnBwfZzIKOY2"
file_path = "bankruptcy_data.csv"

# Download the file from Google Drive
gdown.download(drive_url, file_path, quiet=False)

# Load dataset
df = pd.read_csv(file_path)

# Convert Year to integer
df["Year"] = df["Year"].astype(int)

# Sidebar Filters
bank_types = st.multiselect("Select Bank Type", df["Bank Type"].unique())
filtered_df = df[df["Bank Type"].isin(bank_types)] if bank_types else df

companies = st.multiselect("Select Company Name", filtered_df["Company Name"].unique())
filtered_df = filtered_df[filtered_df["Company Name"].isin(companies)] if companies else filtered_df

# Function to Create a Smooth Trend Plot
def create_smooth_plot(data, y_col, title, y_label):
    data = data.sort_values(by="Year")  # Ensure correct time ordering
    data["Smoothed"] = data.groupby("Company Name")[y_col].transform(lambda x: x.rolling(window=3, min_periods=1).mean())  # Rolling Mean
    
    fig = px.line(data, x="Year", y="Smoothed", color="Company Name", title=title)
    
    # Update layout for better visualization
    fig.update_traces(mode="lines+markers")  # Add markers for data points
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=y_label,
        legend=dict(orientation="h", y=-0.3)  # Move legend below
    )
    return fig

# Create a 2x2 grid layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Generate graphs
with col1:
    st.plotly_chart(create_smooth_plot(filtered_df, "Positive Percentage", "Positive Percentage Trend", "Positive Percentage"), use_container_width=True)

with col2:
    st.plotly_chart(create_smooth_plot(filtered_df, "Negative Percentage", "Negative Percentage Trend", "Negative Percentage"), use_container_width=True)

with col3:
    st.plotly_chart(create_smooth_plot(filtered_df, "Positive Count", "Positive Count Trend", "Positive Count"), use_container_width=True)

with col4:
    st.plotly_chart(create_smooth_plot(filtered_df, "Negative Count", "Negative Count Trend", "Negative Count"), use_container_width=True)
