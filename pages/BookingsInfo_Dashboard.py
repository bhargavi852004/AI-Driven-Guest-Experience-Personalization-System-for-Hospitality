import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import os
from together import Together

# Set Together AI API Key
os.environ["TOGETHER_API_KEY"] = ""

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["bookings_data"]
collection = db["bookings_data"]

# Fetch data
data = list(collection.find())
df = pd.DataFrame(data)

# Data Cleaning
df.dropna(inplace=True)

# Handle string date conversion (dd-mm-yyyy format)
df["check_in_date"] = pd.to_datetime(df["check_in_date"], format='%d-%m-%Y', errors="coerce")
df["check_out_date"] = pd.to_datetime(df["check_out_date"], format='%d-%m-%Y', errors="coerce")

# Calculate stay duration
df['stay_duration'] = (df['check_out_date'] - df['check_in_date']).dt.days

# Remove negative stay durations
df = df[df['stay_duration'] >= 0]

# Age group categorization
def categorize_age(age):
    if age < 20:
        return '15-20'
    elif age < 25:
        return '20-25'
    elif age < 30:
        return '25-30'
    elif age < 35:
        return '30-35'
    elif age < 40:
        return '35-40'
    else:
        return '40+'

df['age_range'] = df['age'].apply(categorize_age)

# Extract Month
df['month'] = df['check_in_date'].dt.month_name()

# Create a new column for classification
df['booked_with_points'] = df['booked_through_points'].apply(lambda x: 'Booked Through Points' if x > 0 else 'Not Booked Through Points')

# Count occurrences
points_count = df['booked_with_points'].value_counts().reset_index()
points_count.columns = ['Type', 'Count']

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🏨 Hotel Bookings Dashboard")

# Sidebar for plot selection
plot_choice = st.sidebar.radio(
    "📊 Choose a visualization:",
    ["Cuisine Preference", "Age Group Distribution", "Stay Duration", "Monthly Bookings", "Booked Through Points"]
)

# Function to render selected plot and extract data summary
plot_data_summary = None
if plot_choice == "Cuisine Preference":
    fig = px.pie(df, names='Preferred Cusine', title='Preferred Cuisine Distribution', color_discrete_sequence=px.colors.sequential.Plasma)
    plot_data_summary = df['Preferred Cusine'].value_counts().to_dict()

elif plot_choice == "Age Group Distribution":
    fig = px.histogram(df, x='age_range', title='Age Group Distribution', color='age_range', color_discrete_sequence=px.colors.qualitative.Pastel)
    plot_data_summary = df['age_range'].value_counts().to_dict()

elif plot_choice == "Stay Duration":
    fig = px.histogram(df, x='stay_duration', title='Stay Duration Distribution', color_discrete_sequence=px.colors.sequential.Rainbow)
    plot_data_summary = df['stay_duration'].describe().to_dict()

elif plot_choice == "Monthly Bookings":
    monthly_data = df.groupby('month').size().reset_index(name='Bookings')
    fig = px.bar(monthly_data, x='month', y='Bookings', title='Monthly Bookings', color='month', color_discrete_sequence=px.colors.qualitative.Pastel)
    plot_data_summary = monthly_data.to_dict()

elif plot_choice == "Booked Through Points":
    fig = px.pie(points_count, names='Type', values='Count', title='Booked Through Points Distribution', color_discrete_sequence=['#FF5733', '#33FF57'])
    plot_data_summary = points_count.to_dict()

# Layout: Graph on the left, AI Insights on the right
col1, col2 = st.columns([3, 1])

# Display plot
with col1:
    st.plotly_chart(fig, use_container_width=True)

# Fetch insights from Together AI
with col2:
    st.subheader("📈 Graph Insights")

    if st.button("Explain this Graph"):
        together_client = Together()
        response = together_client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{
                "role": "user",
                "content": f"Analyze the following data summary: {plot_data_summary}. The plot shows '{plot_choice}'. Provide a concise and professional insight."
            }]
        )

        # Correctly access the AI-generated response
        explanation = response.choices[0].message.content
        st.write(explanation)

# Additional Quick Insights
st.subheader("🔍 Quick Insights")
st.write("✅ Most Preferred Cuisine: ", df['Preferred Cusine'].mode()[0])
st.write("💰 Average Stay Duration: ", round(df['stay_duration'].mean(), 2), "days")
st.write("🔢 Total Bookings: ", len(df))
