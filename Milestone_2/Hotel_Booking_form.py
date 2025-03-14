import streamlit as st
from datetime import date
import pandas as pd
import random  
import joblib
import xgboost
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sklearn.preprocessing import OneHotEncoder
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

def generate_coupon():
    return "HOTEL" + str(random.randint(1000, 9999))

def send_email(name, email, checkin_date, checkout_date, preferred_cuisine,coupon_code):
    sender_email = "ex@gmail.com"  # Replace with your email
    sender_password = "password"  # Replace with your email password
    subject = "Hotel Booking Confirmation"
    body = f"""
    Dear {name},

    Your hotel booking has been confirmed!
    
    Check-in Date: {checkin_date}
    Check-out Date: {checkout_date}
    Preferred Cuisine: {preferred_cuisine}
    
    🎉Use this coupon code for discounts on your meals: {coupon_code}
    
    Thank you for choosing our service!
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        st.success("🎉 Check your Mail for Coupon Code for Discounts and Booking Confirmation")
    except Exception as e:
        st.error(f"⚠️ Email could not be sent: {str(e)}")

# Title
st.title("🏨 Hotel Booking Form")

# Ask if the customer has a customer_id
has_customer_id = st.radio("Do you have a Customer ID?", ("Yes", "No"))

if has_customer_id == "Yes":
    customer_id = st.text_input("Enter your Customer ID", "")
else:
    customer_id = random.randint(10001, 99999)
    st.write(f"Your generated Customer ID: {customer_id}")

# User Inputs
name = st.text_input("Enter your name", "")
email = st.text_input("Enter your email", "")  
checkin_date = st.date_input("Check-in Date", min_value=date.today())
checkout_date = st.date_input("Check-out Date", min_value=checkin_date)
age = st.number_input("Enter your age", min_value=18, max_value=120, step=1)
stayers = st.number_input("How many stayers in total?", min_value=1, max_value=3, step=1)
cuisine_options = ["South Indian", "North Indian", "Multi"]
preferred_cuisine = st.selectbox("Preferred Cuisine", cuisine_options)
preferred_booking = st.selectbox("Do you want to book through points?", ["Yes", "No"])
special_requests = st.text_area("Any Special Requests? (Optional)", "")

# Submit Button
if st.button("Submit Booking"):
    if name and customer_id and email:
        new_data = {
            'customer_id': int(customer_id),
            'Preferred Cusine': preferred_cuisine,
            'age': age,
            'check_in_date': checkin_date,
            'check_out_date': checkout_date,
            'booked_through_points': 1 if preferred_booking == 'Yes' else 0,
            'number_of_stayers': stayers,
            'email': email
        }

        new_df = pd.DataFrame([new_data])
        new_df['check_in_date'] = pd.to_datetime(new_df['check_in_date'])
        new_df['check_out_date'] = pd.to_datetime(new_df['check_out_date'])
        new_df['check_in_day'] = new_df['check_in_date'].dt.dayofweek
        new_df['check_out_day'] = new_df['check_out_date'].dt.dayofweek
        new_df['check_in_month'] = new_df['check_in_date'].dt.month
        new_df['check_out_month'] = new_df['check_out_date'].dt.month
        new_df['stay_duration'] = (new_df['check_out_date'] - new_df['check_in_date']).dt.days

        # Store in MongoDB about the information of New Bookings
        db = client["hotel_guests"]
        new_bookings_collection = db["new_bookings"]
        new_bookings_collection.insert_one(new_df.iloc[0].to_dict())

        # Load feature datasets
        data_files = {
            "age_features": "age_features.xlsx",
            "cuisine_features": "cuisine_features.xlsx",
            "customer_features": "customer_features.xlsx",
            "customer_behaviour_features": "customer_behaviour_features.xlsx",
            "customer_recency_features": "customer_recency_features.xlsx",
            "loyalty_features": "loyalty_features.xlsx",
            "stayed_features": "stayed_features.xlsx"
        }
        
        data_frames = {key: pd.read_excel(value) for key, value in data_files.items()}

        # Merge Features
        for df_name, df in data_frames.items():
            if 'customer_id' in df.columns:
                new_df = new_df.merge(df, on="customer_id", how="left")
            elif 'Preferred Cusine' in df.columns:
                new_df = new_df.merge(df, on="Preferred Cusine", how="left")
            elif 'age' in df.columns:
                new_df = new_df.merge(df, on="age", how="left")
            elif 'number_of_stayers' in df.columns:
                new_df = new_df.merge(df, on="number_of_stayers", how="left")

        # Drop unnecessary columns
        new_df.drop(['customer_id', 'check_in_date', 'check_out_date'], axis=1, inplace=True)

        # Load encoder
        encoder = joblib.load('encoder.pkl')

        # Ensure categorical columns exist before encoding
        categorical_cols = list(encoder.feature_names_in_)  
        for col in categorical_cols:
            if col not in new_df.columns:
                new_df[col] = "Unknown"

        # Remove extra columns that were not seen during encoder training
        new_df = new_df[categorical_cols]

        # Perform encoding
        encoded_test = encoder.transform(new_df)
        encoded_test_df = pd.DataFrame(encoded_test, columns=encoder.get_feature_names_out())

        # Merge encoded features with the rest of the dataframe
        new_df = pd.concat([new_df.drop(columns=categorical_cols), encoded_test_df], axis=1)

        # Load expected feature names from `features.xlsx`
        expected_features = list(pd.read_excel('features.xlsx')[0])
        
        # Ensure all expected features exist and fill missing ones with 0
        for feature in expected_features:
            if feature not in new_df.columns:
                new_df[feature] = 0

        # Reorder columns to match model input
        new_df = new_df[expected_features]

        # Load model and make predictions
        model = joblib.load('xgb_model_dining.pkl')
        y_pred_prob = model.predict_proba(new_df)

        # Load label encoder
        label_encoder = joblib.load('label_encoder.pkl')
        dish_names = label_encoder.classes_

        # Get top 3 predictions
        top_3_indices = np.argsort(-y_pred_prob, axis=1)[:, :3]
        top_3_dishes = dish_names[top_3_indices]

        # Generate Coupon Code
        coupon_code = generate_coupon()

        # Send Email Notification
        send_email(name, email, checkin_date, checkout_date, preferred_cuisine,coupon_code)

        #Display Booking
        st.success(f"✅ Booking Confirmed for {name} (Customer ID: {customer_id})!")
        st.write(f"**Check-in:** {checkin_date}")
        st.write(f"**Check-out:** {checkout_date}")
        st.write(f"**Age:** {age}")
        st.write(f"**Preferred Cuisine:** {preferred_cuisine}")
        st.write(f"🍽 **Recommended Dishes:** {', '.join(top_3_dishes[0])}")
        if special_requests:
            st.write(f"**Special Requests:** {special_requests}")
    else:
        st.warning("⚠️ Please enter your name, Customer ID, and Email to proceed!")
