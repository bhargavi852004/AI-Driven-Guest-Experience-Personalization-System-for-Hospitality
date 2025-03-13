from dash import Dash, dcc, html, Output, Input
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["hotel_guests"]
collection = db["dining_info"]

# Fetch data
data = list(collection.find())
df = pd.DataFrame(data)

# Data cleaning
df.dropna(inplace=True)
df.columns = df.columns.str.strip()
df["check_in_date"] = pd.to_datetime(df["check_in_date"].apply(lambda x: x["$date"] if isinstance(x, dict) and "$date" in x else None), errors="coerce")
df["check_out_date"] = pd.to_datetime(df["check_out_date"].apply(lambda x: x["$date"] if isinstance(x, dict) and "$date" in x else None), errors="coerce")
df["order_time"] = pd.to_datetime(df["order_time"].apply(lambda x: x["$date"] if isinstance(x, dict) and "$date" in x else None), errors="coerce")
df['price_for_1'] = pd.to_numeric(df['price_for_1'], errors='coerce')
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')

# Calculate stay duration
df['stay_duration'] = (df['check_out_date'] - df['check_in_date']).dt.days.fillna(0)

# Define age groups
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

if 'age' in df.columns:
    df['age_range'] = df['age'].apply(categorize_age)

# Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Enhanced Dining Dashboard 🍽️"),
    dcc.Graph(id='most-dishes-stay-duration'),
    dcc.Graph(id='avg-spending-per-customer'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='revenue-by-cuisine'),
    dcc.Graph(id='cuisine-by-age-group'),
    dcc.Graph(id='price-distribution'),
    dcc.Graph(id='most-ordered-dishes'),
    dcc.Graph(id='most-ordered-dishes-by-age')
])

@app.callback(
    [
        Output('most-dishes-stay-duration', 'figure'),
        Output('avg-spending-per-customer', 'figure'),
        Output('pie-chart', 'figure'),
        Output('revenue-by-cuisine', 'figure'),
        Output('cuisine-by-age-group', 'figure'),
        Output('price-distribution', 'figure'),
        Output('most-ordered-dishes', 'figure'),
        Output('most-ordered-dishes-by-age', 'figure')
    ],
    Input('most-dishes-stay-duration', 'figure')
)
def update_graphs(_):
    # Most Preferred Dishes Based on Stay Duration
    dishes_by_stay = df.groupby(['stay_duration', 'dish']).size().reset_index(name='Count')
    stay_dish_fig = px.bar(dishes_by_stay, 
                           x='stay_duration', 
                           y='Count', 
                           color='dish', 
                           title='Most Preferred Dishes Based on Stay Duration',
                           barmode='group')

    # Average Spending Per Customer (Bar Chart)
    avg_spending = df.groupby('Preferred Cusine')['price_for_1'].mean().reset_index()
    spending_fig = px.bar(avg_spending, 
                          x='Preferred Cusine', 
                          y='price_for_1',
                          title='Average Spending Per Cuisine', 
                          color='price_for_1')

    # Pie Chart: Average Dining Cost by Cuisine
    pie_fig = px.pie(df, values='price_for_1', names='Preferred Cusine', title='Average Dining Cost by Cuisine')

    # Revenue by Cuisine
    revenue_cuisine = df.groupby('Preferred Cusine')['price_for_1'].sum().reset_index()
    revenue_fig = px.bar(revenue_cuisine, x='Preferred Cusine', y='price_for_1', title='Total Revenue by Cuisine', color='price_for_1')

    # Top Preferred Cuisine by Age Group
    cuisine_age = df.groupby(['age_range', 'Preferred Cusine']).size().reset_index(name='Count')
    cuisine_age_fig = px.bar(cuisine_age, x='age_range', y='Count', color='Preferred Cusine', barmode='group', title='Preferred Cuisine by Age Group')

    # Price Distribution of Dishes
    price_fig = px.histogram(df, x='price_for_1', nbins=30, title='Price Distribution of Dishes', color_discrete_sequence=['#FFA07A'])

    # Most Ordered Dishes
    most_dishes = df.groupby('dish').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    most_dishes_fig = px.bar(most_dishes, x='dish', y='Count', title='Most Ordered Dishes', orientation='v')

    # Most Ordered Dishes by Age Range
    age_dish = df.groupby(['age_range', 'dish']).size().reset_index(name='Count')
    age_dish_fig = px.bar(age_dish, x='age_range', y='Count', color='dish', barmode='group', title='Most Ordered Dishes by Age Range')

    return stay_dish_fig, spending_fig, pie_fig, revenue_fig, cuisine_age_fig, price_fig, most_dishes_fig, age_dish_fig

if __name__ == '__main__':
    app.run_server(debug=True)
