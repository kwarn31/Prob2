# Now let's build the dashboard!
import streamlit as st
import pandas as pd 
import plotly.express as px 

# Title of the app
st.title("University Dashboard")

# Select Year with Slider
selected_year = st.slider("Select Year:", int(df["Year"].min()), int(df["Year"].max()), int(df["Year"].min()))

# KPIs 
# Total applications, admissions, and enrollments per term
# Retention rate trends over time
# Student satisfaction scores over the years
# Enrollment breakdown by department (Engineering, Business, Arts, Science)
# Comparison between Spring vs. Fall term trends.
# Compare trends between departments, retention rates, and satisfaction levels.

# Filter Data by Selected Year
filtered_data = df[df["Year"] == selected_year]

# Melt Data for Plotly
data_melted = filtered_data.melt(id_vars=["Year", "Term"], 
                                 var_name="Field", value_name="Enrollment")

# Create Grouped Bar Chart
fig = px.bar(data_melted, x="Term", y="Enrollment", color="Field", 
             barmode="group", title=f"Enrollment by Field for {selected_year}")

# Display Chart
st.title("Enrollment Trends by Field")
st.plotly_chart(fig)
