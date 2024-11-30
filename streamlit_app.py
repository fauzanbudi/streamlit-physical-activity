import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandasql as ps
from pathlib import Path

# Get all records
DATA_FILENAME = Path(__file__).parent/'demo.csv'
data = pd.read_csv(DATA_FILENAME)
df = pd.DataFrame(data)

DATA_ACT_FILENAME = Path(__file__).parent/'activity.csv'
data_act = pd.read_csv(DATA_ACT_FILENAME)
act_df = pd.DataFrame(data_act)

# SQL query to join the DataFrames on the 'id' column
query = """
SELECT 
  a.id,
  a.Sedentary,
  a.Light,
  a.Moderate,
  a.Vigorous,
  a.Date,
  a.Timepoint,
  d.weight,
  d.height,
  d.gender,
  d.race,
  d.ethnic,
  d.birthdate,
  d.bmi
FROM act_df a 
LEFT JOIN df d ON d.id = a.id
"""

# Merged data
activity_df = ps.sqldf(query)

# Convert birthdate to age
current_year = 2024
activity_df['age'] = current_year - activity_df['birthdate']

# Sidebar for page selection
page = st.sidebar.selectbox("Choose a page", ["Demographics", "Physical Activity"])

if page == "Demographics":
    st.title("Demographic Dashboard")

    # Filters
    gender_filter = st.sidebar.multiselect("Select Gender", options=activity_df['gender'].dropna().unique(), default=activity_df['gender'].dropna().unique())
    race_filter = st.sidebar.multiselect("Select Race", options=activity_df['race'].unique(), default=activity_df['race'].unique())
    ethnic_filter = st.sidebar.multiselect("Select Ethnicity", options=activity_df['ethnic'].unique(), default=activity_df['ethnic'].unique())
    age_filter = st.sidebar.slider("Select Age Range", min_value=int(activity_df['age'].min()), max_value=int(activity_df['age'].max()), value=(int(activity_df['age'].min()), int(activity_df['age'].max())))

    # Sidebar footer with hyperlink
    st.sidebar.markdown(
        """
        ---
        Created using streamlit python and a public dataset from data.gov of the US government. [Link to Dataset](https://catalog.data.gov/dataset/data-from-the-influence-of-active-video-game-play-upon-physical-activity-and-screen-based--33694)
        
        Fauzan Budi Prasetya, fauzanbudiprasetya@gmail.com, [Linkedin](https://www.linkedin.com/in/fauzan-budi-prasetya/)
        """
    )

    # Apply filters
    filtered_df = activity_df[
        (activity_df['gender'].isin(gender_filter)) &
        (activity_df['race'].isin(race_filter)) &
        (activity_df['ethnic'].isin(ethnic_filter)) &
        (activity_df['age'].between(age_filter[0], age_filter[1]))
    ]


    # Metric 1: Average Weight by Race
    st.subheader("Average Weight by Race")
    if not filtered_df['weight'].isnull().all():
        avg_weight_by_race = filtered_df.groupby('race')['weight'].mean()
        st.bar_chart(avg_weight_by_race)
    else:
        st.write("No weight data available.")

    # Metric 2: Average Height by Race
    st.subheader("Average Height by Race")
    if not filtered_df['height'].isnull().all():
        avg_height_by_race = filtered_df.groupby('race')['height'].mean()
        st.bar_chart(avg_height_by_race)
    else:
        st.write("No height data available.")

    # Metric 1: Average BMI by Gender
    st.subheader("Average BMI by Gender")
    if not filtered_df['bmi'].isnull().all():
        avg_bmi_by_gender = filtered_df.groupby('gender')['bmi'].mean()
        st.bar_chart(avg_bmi_by_gender)
    else:
        st.write("No BMI data available.")

    # Metric 1: Average BMI by Ethnicity
    st.subheader("Average BMI by Ethnicity")
    if not filtered_df['bmi'].isnull().all():
        avg_bmi_by_ethnicity = filtered_df.groupby('ethnic')['bmi'].mean()
        st.bar_chart(avg_bmi_by_ethnicity)
    else:
        st.write("No BMI data available.")

    # Metric 3: Average BMI by Race
    st.subheader("Average BMI by Race")
    if not filtered_df['bmi'].isnull().all():
        avg_bmi_by_race = filtered_df.groupby('race')['bmi'].mean()
        st.bar_chart(avg_bmi_by_race)
    else:
        st.write("No BMI data available.")

    # Metric 4: BMI Distribution using Histogram
    st.subheader("BMI Distribution")
    if not filtered_df['bmi'].isnull().all():
        bmi_values = filtered_df['bmi'].dropna()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')  
        ax.set_facecolor('black') 
        ax.hist(bmi_values, bins=10, color='skyblue', edgecolor='black')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        st.pyplot(fig)
    else:
        st.write("No BMI data available.")

elif page == "Physical Activity":
    st.title("Physical Activity Dashboard")

    # Filters
    gender_filter = st.sidebar.multiselect("Select Gender", options=activity_df['gender'].dropna().unique(), default=activity_df['gender'].dropna().unique())
    race_filter = st.sidebar.multiselect("Select Race", options=activity_df['race'].unique(), default=activity_df['race'].unique())
    ethnic_filter = st.sidebar.multiselect("Select Ethnicity", options=activity_df['ethnic'].unique(), default=activity_df['ethnic'].unique())
    age_filter = st.sidebar.slider("Select Age Range", min_value=int(activity_df['age'].min()), max_value=int(activity_df['age'].max()), value=(int(activity_df['age'].min()), int(activity_df['age'].max())))

    # Sidebar footer with hyperlink
    st.sidebar.markdown(
        """
        ---
        Created using streamlit python and a public dataset from data.gov of the US government. [Link to Dataset](https://catalog.data.gov/dataset/data-from-the-influence-of-active-video-game-play-upon-physical-activity-and-screen-based--33694)
        
        Fauzan Budi Prasetya, fauzanbudiprasetya@gmail.com, [Linkedin](https://www.linkedin.com/in/fauzan-budi-prasetya/)
        """
    )

    # Apply filters
    filtered_df = activity_df[
        (activity_df['gender'].isin(gender_filter)) &
        (activity_df['race'].isin(race_filter)) &
        (activity_df['ethnic'].isin(ethnic_filter)) &
        (activity_df['age'].between(age_filter[0], age_filter[1]))
    ]

    # Metric 1: Average Sedentary Minutes by Timepoint
    st.subheader("Average Sedentary Minutes by Timepoint")
    avg_sedentary_by_timepoint = filtered_df.groupby('Timepoint')['Sedentary'].mean()
    st.line_chart(avg_sedentary_by_timepoint)

    # Metric 2: Average Light Minutes by Timepoint
    st.subheader("Average Light Minutes by Timepoint")
    avg_light_by_timepoint = filtered_df.groupby('Timepoint')['Light'].mean()
    st.line_chart(avg_light_by_timepoint)

    # Metric 2: Average Moderate Minutes by Timepoint
    st.subheader("Average Moderate Minutes by Timepoint")
    avg_moderate_by_timepoint = filtered_df.groupby('Timepoint')['Moderate'].mean()
    st.line_chart(avg_moderate_by_timepoint)

    # Metric 2: Average Vigorous Minutes by Timepoint
    st.subheader("Average Vigorous Minutes by Timepoint")
    avg_vigorous_by_timepoint = filtered_df.groupby('Timepoint')['Vigorous'].mean()
    st.line_chart(avg_vigorous_by_timepoint)
    
    # Metric 3: BMI Distribution using Histogram
    st.subheader("Distribution of Sedentary Activity Minutes")
    if not filtered_df['Sedentary'].isnull().all():
        sedentary_values = filtered_df['Sedentary'].dropna()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')  
        ax.set_facecolor('black') 
        ax.hist(sedentary_values, bins=10, color='skyblue', edgecolor='black')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        st.pyplot(fig)
    else:
        st.write("No Sedentary Activity data available.")

    # Metric 4: BMI Distribution using Histogram
    st.subheader("Distribution of Light Activity Minutes")
    if not filtered_df['Light'].isnull().all():
        light_values = filtered_df['Light'].dropna()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')  
        ax.set_facecolor('black') 
        ax.hist(light_values, bins=10, color='skyblue', edgecolor='black')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        st.pyplot(fig)
    else:
        st.write("No Light Activity data available.")

    # Metric 5: BMI Distribution using Histogram
    st.subheader("Distribution of Moderate Activity Minutes")
    if not filtered_df['Moderate'].isnull().all():
        moderate_values = filtered_df['Moderate'].dropna()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')  
        ax.set_facecolor('black') 
        ax.hist(moderate_values, bins=10, color='skyblue', edgecolor='black')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        st.pyplot(fig)
    else:
        st.write("No Moderate Activity data available.")
      
    # Metric 5: BMI Distribution using Histogram
    st.subheader("Distribution of Vigorous Activity Minutes")
    if not filtered_df['Vigorous'].isnull().all():
        vigorous_values = filtered_df['Vigorous'].dropna()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')  
        ax.set_facecolor('black') 
        ax.hist(vigorous_values, bins=10, color='skyblue', edgecolor='black')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        st.pyplot(fig)
    else:
        st.write("No Moderate Activity data available.")