# Now let's build the dashboard!
import streamlit as st
import pandas as pd 
import plotly.express as px 

# Import data
df = pd.read_csv("university_student_dashboard_data.csv")


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Overall"])

# Home Page
if page == "Home":
    st.title("🏛️ University Dashboard")
    st.write("Welcome to the University Dashboard! ")

    # Title of the app
    st.title("Yearly Dashboard")

    # Select Year with Slider
    selected_year = st.slider("Select Year:", int(df["Year"].min()), int(df["Year"].max()), int(df["Year"].min()))

    # Sidebar Filter for Term (Spring or Fall) 
    st.sidebar.header("Filters")
    term_filter = st.sidebar.selectbox("Select Term", ['All'] + list(df['Term'].unique()))
    if term_filter != 'All':
        df = df[df['Term'] == term_filter]
    
    # KPIs 
    # Total applications, admissions, and enrollments per term DONE
    # Retention rate trends over time  DONE
    # Student satisfaction scores over the years DONE
    # Enrollment breakdown by department (Engineering, Business, Arts, Science)
    # Comparison between Spring vs. Fall term trends. DONE
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
    data_melted = filtered_data.melt(id_vars=["Term"], 
                                 value_vars=["Applications", "Admitted", "Enrolled"], 
                                 var_name="Stage", value_name="Count")

    # Adjust x-axis based on term selection
    if term_filter == "All":
        x_axis = "Term"  # Show term-wise bars when all terms are selected
    else:
        x_axis = "Stage"  # Show stage-wise bars when a single term is selected

    # Create Grouped Bar Chart
    fig = px.bar(data_melted, x=x_axis, y="Count", color="Stage", 
                 barmode="group", title=f"Applications, Admissions & Enrollments in {selected_year} ({term_filter})")

    # Display in Streamlit
    st.title("University Admissions Overview")
    st.plotly_chart(fig)


    # Melt Data for Plotly
    data_melted = filtered_data.melt(id_vars=["Year", "Term"], 
                                 var_name="Field", value_name="Enrollment")

    # Create Grouped Bar Chart
    fig = px.bar(data_melted, x="Term", y="Enrollment", color="Field", 
                 barmode="group", title=f"Enrollment by Field for {selected_year}")

    # Display Chart
    st.title("Enrollment Trends by Field")
    st.plotly_chart(fig)

# Overall Page
elif page == "Overall":
      
        st.title("📊 Overall Overview")
        # the data seems to be the same for the spring and the fall for many of the columns... 
        # going to keep only the fall values for these charts because I think I will be doubling the numbers otherwise 
        unique_years_df = df.drop_duplicates(subset="Year", keep="first")
    
        # Convert Year column to integer
        df["Year"] = unique_years_df["Year"].astype(int)
        overall_trends_1 = unique_years_df.groupby("Year")[["Applications", "Admitted", "Enrolled"]].sum().reset_index()


        # Plot 1 
        fig = px.line(overall_trends_1, x="Year", y=["Applications", "Admitted", "Enrolled"],
                    markers=True, title="Enrollment Trends Over Time")
        # Fix Year axis formatting
        fig.update_layout(xaxis=dict(tickmode="linear", tick0=overall_trends["Year"].min(), dtick=1))
        st.plotly_chart(fig)
    
        # Plot 2
        overall_trends_2 = unique_years_df.groupby("Year")[["Student Satisfaction (%)", "Retention Rate (%)"]].sum().reset_index()
        fig = px.line(overall_trends_2, x="Year", y=["Student Satisfaction (%)", "Retention Rate (%)"],
                    markers=True, title="Satisfaction and Retention over Time")
        # Fix Year axis formatting
        fig.update_layout(xaxis=dict(tickmode="linear", tick0=overall_trends["Year"].min(), dtick=1))
        st.plotly_chart(fig)

        # Plot 3 
        overall_trends_3 = unique_years_df.groupby("Year")[["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]].sum().reset_index()
        fig = px.line(overall_trends_3, x="Year", y=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"],
                    markers=True, title="Enrollment by Department")
        # Fix Year axis formatting
        fig.update_layout(xaxis=dict(tickmode="linear", tick0=overall_trends["Year"].min(), dtick=1))
        st.plotly_chart(fig)

