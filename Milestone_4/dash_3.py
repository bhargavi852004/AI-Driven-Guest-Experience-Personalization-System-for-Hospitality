from pymongo import MongoClient
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

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

# Step 3: Build Dashboard
app = dash.Dash(__name__)

# Pie chart for sentiment analysis (Placeholder data)
sentiment_data = {
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Count": [50, 30, 20]
}

sentiment_df = pd.DataFrame(sentiment_data)

# Histogram for rating distribution with different colors per range
fig_hist = px.histogram(df, x="Rating", nbins=10, title="Rating Distribution", color=df['Rating'].apply(lambda x: 'Low' if x < 4 else 'Medium' if x < 7 else 'High'), color_discrete_map={"Low": "red", "Medium": "yellow", "High": "green"})

# Pie chart for sentiment analysis
fig_pie = px.pie(sentiment_df, values='Count', names='Sentiment', title="Sentiment Analysis", color_discrete_sequence=px.colors.qualitative.Pastel)

# Review trends over time with color by month
month_colors = px.colors.qualitative.Set3
fig_review_trend = px.histogram(df, x="review_date", title="Review Trends Over Time", color=df['review_date'].dt.month.astype(str), color_discrete_sequence=month_colors)

# Bar chart for overall average rating distribution with different colors per rating
rating_counts = df['Rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']
fig_avg_rating = px.bar(rating_counts, x="Rating", y="Count", title="Overall Customer Rating Distribution", color="Rating", color_continuous_scale="Turbo")

# Layout
app.layout = html.Div(children=[
    html.H1("Customer Review Analysis Dashboard"),
    dcc.Graph(figure=fig_pie),
    dcc.Graph(figure=fig_hist),
    dcc.Graph(figure=fig_review_trend),
    dcc.Graph(figure=fig_avg_rating),
])

if __name__ == '__main__':
    app.run_server(debug=True)