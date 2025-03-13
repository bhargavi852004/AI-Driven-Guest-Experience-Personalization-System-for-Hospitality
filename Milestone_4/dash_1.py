from dash import Dash, dcc, html, Output, Input
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

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

# Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Hotel Bookings Dashboard 🏨"),

    dcc.Graph(id='cuisine-preference'),
    dcc.Graph(id='age-group-distribution'),
    dcc.Graph(id='stay-duration-distribution'),
    dcc.Graph(id='bookings-by-month'),
    dcc.Graph(id='booked-through-points')
])

@app.callback(
    [
        Output('cuisine-preference', 'figure'),
        Output('age-group-distribution', 'figure'),
        Output('stay-duration-distribution', 'figure'),
        Output('bookings-by-month', 'figure'),
        Output('booked-through-points', 'figure')
    ],
    Input('cuisine-preference', 'figure')  # Dummy input to trigger the callback
)
def update_graphs(_):
    # Cuisine Preference
    cuisine_fig = px.pie(df, names='Preferred Cusine', title='Preferred Cuisine Distribution', color_discrete_sequence=px.colors.sequential.Plasma)

    # Age Group Distribution
    age_fig = px.histogram(df, x='age_range', title='Age Group Distribution', color='age_range', color_discrete_sequence=px.colors.qualitative.Pastel)

    # Stay Duration Analysis
    stay_fig = px.histogram(df, x='stay_duration', title='Stay Duration Distribution', color_discrete_sequence=px.colors.sequential.Rainbow)

    # Bookings by Month
    bookings_fig = px.bar(
        df.groupby('month').size().reset_index(name='Bookings'),
        x='month',
        y='Bookings',
        title='Monthly Bookings',
        color='month',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Booked Through Points (Pie Chart)
    points_pie_fig = px.pie(
        points_count, 
        names='Type', 
        values='Count', 
        title='Booked Through Points Distribution',
        color_discrete_sequence=['#FF5733', '#33FF57']  # Orange & Green for better visibility
    )

    return cuisine_fig, age_fig, stay_fig, bookings_fig, points_pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)