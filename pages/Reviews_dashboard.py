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
db = client["reviews_data"]
collection = db["reviews_data"]

# Fetch data from MongoDB
data = list(collection.find())
df = pd.DataFrame(data)

# Handle missing values (if any)
df.fillna("", inplace=True)

# Convert date to datetime format, handling errors
df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')

# Pie chart for sentiment analysis (Placeholder data)
sentiment_data = {
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Count": [50, 30, 20]
}

sentiment_df = pd.DataFrame(sentiment_data)

# Histogram for rating distribution with different colors per range
fig_hist = px.histogram(
    df, x="Rating", nbins=10, title="Rating Distribution",
    color=df['Rating'].apply(lambda x: 'Low' if x < 4 else 'Medium' if x < 7 else 'High'),
    color_discrete_map={"Low": "red", "Medium": "yellow", "High": "green"}
)

# Pie chart for sentiment analysis
fig_pie = px.pie(
    sentiment_df, values='Count', names='Sentiment', 
    title="Sentiment Analysis", color_discrete_sequence=px.colors.qualitative.Pastel
)

# Review trends over time with color by month
month_colors = px.colors.qualitative.Set3
fig_review_trend = px.histogram(
    df, x="review_date", title="Review Trends Over Time",
    color=df['review_date'].dt.month.astype(str), color_discrete_sequence=month_colors
)

# Bar chart for overall average rating distribution with different colors per rating
rating_counts = df['Rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']
fig_avg_rating = px.bar(
    rating_counts, x="Rating", y="Count", 
    title="Overall Customer Rating Distribution", color="Rating", color_continuous_scale="Turbo"
)

# Streamlit UI layout
st.set_page_config(layout="wide")

st.title("Customer Review Analysis Dashboard")

# Two-column layout
col1, col2 = st.columns([3, 1])

with col1:
    # Dropdown to select plot
    plot_option = st.selectbox(
        "Choose a plot to display:",
        ("Sentiment Analysis", "Rating Distribution", "Review Trends Over Time", "Overall Rating Distribution")
    )

    # Display the selected plot
    if plot_option == "Sentiment Analysis":
        st.plotly_chart(fig_pie)
        data_summary = sentiment_df.describe().to_dict()
        plot_title = "Sentiment Analysis"

    elif plot_option == "Rating Distribution":
        st.plotly_chart(fig_hist)
        data_summary = df['Rating'].describe().to_dict()
        plot_title = "Rating Distribution"

    elif plot_option == "Review Trends Over Time":
        st.plotly_chart(fig_review_trend)
        data_summary = df['review_date'].describe().to_dict()
        plot_title = "Review Trends Over Time"

    elif plot_option == "Overall Rating Distribution":
        st.plotly_chart(fig_avg_rating)
        data_summary = rating_counts.describe().to_dict()
        plot_title = "Overall Rating Distribution"

# Right section for AI insights
with col2:
    st.write("### 📈 Graph Insights")

    if st.button("Explain the Dashboard"):
        together_client = Together()
        response = together_client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{
                "role": "user",
                "content": f"Explain the insights from this customer review data summary: {data_summary}. The graph shows {plot_title}. Provide a concise and professional summary."
            }]
        )

        # Access the response correctly
        explanation = response.choices[0].message.content
        st.write(explanation)
