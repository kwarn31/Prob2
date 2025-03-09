# Now let's build the dashboard!
import streamlit as st
import pandas as pd 
import plotly.express as px 

# Import data
df = pd.read_csv("university_student_dashboard_data.csv")

# Title of the app
st.title("University Dashboard")

# Select Year with Slider
selected_year = st.slider("Select Year:", int(df["Year"].min()), int(df["Year"].max()), int(df["Year"].min()))

# Sidebar Filter for Term (Spring or Fall) 
st.sidebar.header("Filters")
term_filter = st.sidebar.selectbox("Select Term", ['All'] + list(df['Term'].unique()))
if term_filter != 'All':
    df = df[df['Term'] == term_filter]
    
# KPIs 
# Total applications, admissions, and enrollments per term
# Retention rate trends over time
# Student satisfaction scores over the years
# Enrollment breakdown by department (Engineering, Business, Arts, Science)
# Comparison between Spring vs. Fall term trends.
# Compare trends between departments, retention rates, and satisfaction levels.

# Filter Data by Selected Year and Term 
filtered_data = df[df["Year"] == selected_year]
if term_filter != 'All':
    filtered_data = filtered_data[filtered_data['Term'] == term_filter]

# KPIs
cl1, cl2 = st.columns((2))
with cl1: 
    # Retention Rate 
    st.subheader("Retention Rate (%)")
    retention = filtered_data["Retention Rate (%)"].values[0]
    # Determine color based on satisfaction level
    if retention < 80:
        color = "red"
    elif retention < 85:
        color = "orange"
    else:
        color = "green"
    st.markdown(f"<h3 style='color:{color};'>● {retention:.1f}%</h3>", unsafe_allow_html=True)
with cl2: 
    # Student Satisfaction 
    st.subheader("Student Satisfaction (%)")
    satisfaction = filtered_data["Student Satisfaction (%)"].values[0]
    # Determine color based on satisfaction level
    if satisfaction < 80:
        color = "red"
    elif satisfaction < 85:
        color = "orange"
    else:
        color = "green"
    # with color
    st.markdown(f"<h3 style='color:{color};'>● {satisfaction:.1f}%</h3>", unsafe_allow_html=True)



# Melt Data for Plotly
data_melted = filtered_data.melt(id_vars=["Year", "Term"], 
                                 var_name="Field", value_name="Enrollment")

# Create Grouped Bar Chart
fig = px.bar(data_melted, x="Term", y="Enrollment", color="Field", 
             barmode="group", title=f"Enrollment by Field for {selected_year}")

# Display Chart
st.title("Enrollment Trends by Field")
st.plotly_chart(fig)
