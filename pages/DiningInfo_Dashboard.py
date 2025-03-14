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
db = client["hotel_guests"]
collection = db["dining_info"]

# Fetch data
data = list(collection.find())
df = pd.DataFrame(data)

# Data Cleaning
df.dropna(inplace=True)
df.columns = df.columns.str.strip()
df["check_in_date"] = pd.to_datetime(df["check_in_date"].apply(lambda x: x["$date"] if isinstance(x, dict) and "$date" in x else None), errors="coerce")
df["check_out_date"] = pd.to_datetime(df["check_out_date"].apply(lambda x: x["$date"] if isinstance(x, dict) and "$date" in x else None), errors="coerce")
df["order_time"] = pd.to_datetime(df["order_time"].apply(lambda x: x["$date"] if isinstance(x, dict) and "$date" in x else None), errors="coerce")
df['price_for_1'] = pd.to_numeric(df['price_for_1'], errors='coerce')
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')

# Calculate stay duration
df['stay_duration'] = (df['check_out_date'] - df['check_in_date']).dt.days.fillna(0)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🍴 Hotel Dining Insights Dashboard")

# Dashboard Options
plot_option = st.sidebar.selectbox("Choose Insight to View", [
    "Most Preferred Dishes Based on Stay Duration",
    "Average Spending Per Cuisine",
    "Price Distribution of Dishes",
    "Most Ordered Dishes",
    "Top 5 Dishes by Revenue",
    "Average Dining Cost by Cuisine (Pie Chart)",
])

# Generate Plots
if plot_option == "Most Preferred Dishes Based on Stay Duration":
    data = df.groupby(['stay_duration', 'dish']).size().reset_index(name='Count')
    fig = px.bar(data, x='stay_duration', y='Count', color='dish', barmode='group')
    plot_data_summary = data.describe().to_dict()

elif plot_option == "Average Spending Per Cuisine":
    data = df.groupby('Preferred Cusine')['price_for_1'].mean().reset_index()
    fig = px.bar(data, x='Preferred Cusine', y='price_for_1', title="Average Spending Per Cuisine")
    plot_data_summary = data.describe().to_dict()

elif plot_option == "Price Distribution of Dishes":
    price_dist = df.groupby('dish')['price_for_1'].mean().reset_index()
    fig = px.bar(price_dist, x='dish', y='price_for_1', title='Price Distribution of Dishes', color='price_for_1')
    plot_data_summary = price_dist.describe().to_dict()

elif plot_option == "Most Ordered Dishes":
    data = df.groupby('dish').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    fig = px.bar(data, x='dish', y='Count', title='Most Ordered Dishes')
    plot_data_summary = data.describe().to_dict()

elif plot_option == "Top 5 Dishes by Revenue":
    data = df.groupby('dish')['price_for_1'].sum().reset_index().sort_values(by='price_for_1', ascending=False).head(5)
    fig = px.bar(data, x='dish', y='price_for_1', title='Top 5 Dishes by Revenue')
    plot_data_summary = data.describe().to_dict()

elif plot_option == "Average Dining Cost by Cuisine (Pie Chart)":
    fig = px.pie(df, values='price_for_1', names='Preferred Cusine', title='Average Dining Cost by Cuisine')
    plot_data_summary = df.groupby('Preferred Cusine')['price_for_1'].sum().to_dict()

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
                "content": f"Analyze the following data summary: {plot_data_summary}. The plot shows '{plot_option}'. Provide a concise and professional insight."
            }]
        )

        # Correctly access the AI-generated response
        explanation = response.choices[0].message.content
        st.write(explanation)

# Additional Quick Insights
st.subheader("🔍 Quick Insights")
st.write("✅ Most Ordered Cuisine: ", df['Preferred Cusine'].mode()[0])
st.write("💰 Highest Spending Dish: ", df.loc[df['price_for_1'].idxmax()]['dish'])
st.write("📈 Average Order Cost: ₹", round(df['price_for_1'].mean(), 2))
