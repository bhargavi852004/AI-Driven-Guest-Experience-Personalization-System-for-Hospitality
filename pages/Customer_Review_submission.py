import streamlit as st
import pandas as pd
import datetime
import random
import os
import numpy as np
from pinecone import Pinecone
from together import Together
from langchain_together import TogetherEmbeddings
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText

# ✅ Set API Keys
TOGETHER_API_KEY = "cd798c47738b9e78e43f073081ab4859ff2533b03ab67b1e630849e9037acf49"
PINECONE_API_KEY = "pcsk_2VGEWR_GToh8JpFKqZipqezYuym65c5Y1okY3BneJetVqVHE3b1JDvCzQBg5bmmbyHSkJX"
PINECONE_HOST = "hotelreview-778bu11.svc.aped-4627-b74a.pinecone.io"

# ✅ Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_HOST)

# ✅ Set Together API Key
os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY
embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval")

# ✅ Define the Excel file
file_name = "reviews_data.xlsx"

# ✅ Load dataset or create if not exists
if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame(columns=["review_id", "customer_id", "review_date", "Review", "Rating", "review_date_numeric"])
    


# ✅ Function to generate a random 4-digit ID
def generate_id():
    return random.randint(1000, 9999)

# ✅ Function to analyze sentiment
def get_sentiment(review_text):
    analysis = TextBlob(review_text)
    return analysis.sentiment.polarity

# ✅ Function to send email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(room_number, review_text, sentiment_score):
    sender_email = "projectb1885@gmail.com"
    receiver_email = "22nn1a0599.bhargavi@gmail.com"
    password = "uiqo vaau gpcz uepk"

    subject = "Negative Review Alert 🚨"
    body = f"Room Number: {room_number}\nReview: {review_text}\nSentiment Score: {sentiment_score}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


# ✅ Streamlit UI
st.set_page_config(page_title="Hotel Reviews", page_icon="⭐", layout="centered")
st.title("📢 Customer Review Submission")
st.markdown("Share your thoughts about our service! Your feedback helps us improve. 💬")

# User inputs
review_text = st.text_area("✍️ Write your review:", help="Describe your experience with us.")
rating = st.slider("⭐ Rate us (1-10)", 1, 10, 5)
room_number = st.text_input("🏨 Room Number (if staying):", "")

if st.button("✅ Submit Review", use_container_width=True):
    if review_text.strip():
        # ✅ Generate new review ID & customer ID
        new_review_id = generate_id()
        customer_id = generate_id()

        # ✅ Get current timestamp and convert it to numeric format
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        numeric_timestamp = int(datetime.datetime.now().timestamp())

        # ✅ Analyze sentiment
        sentiment_score = get_sentiment(review_text)

        # ✅ Prepare new entry
        new_entry = pd.DataFrame([[new_review_id, customer_id, timestamp, review_text, rating, numeric_timestamp]],
                                 columns=df.columns)

        # ✅ Append to dataset & save
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(file_name, index=False)

        # ✅ Generate Embeddings using Together AI
        review_embedding = embeddings.embed_query(review_text)

        # ✅ Store review in Pinecone
        index.upsert(
            vectors=[(str(new_review_id), review_embedding, {"review_id": new_review_id, "customer_id": customer_id, "rating": rating})]
        )

        # ✅ Send email if negative sentiment and customer is staying
        if sentiment_score < 0 and room_number:
            send_email(room_number, review_text, sentiment_score)

        # 🎉 Display Success Message with Review Details
        st.success("✅ Review submitted successfully!")

        st.markdown("### 📌 Submitted Review Details")
        st.write(f"**Review ID:** {new_review_id}")
        st.write(f"**Customer ID:** {customer_id}")
        st.write(f"**Date:** {timestamp}")
        st.write(f"**Review:** {review_text}")
        st.write(f"**Rating:** {rating} ⭐")
        st.write(f"**Sentiment Score:** {sentiment_score}")

        st.markdown("---")
        st.markdown("### 📂 Data Storage Confirmation")
        st.success("✅ Your review has been successfully stored in our dataset!")
        st.info("📌 It is saved in `reviews_data.xlsx`.")

        st.markdown("### 🔗 Vector Database Confirmation")
        st.success("✅ Your review embedding has been successfully stored in Pinecone!")
        st.info("📌 It is indexed under the ID: " + str(new_review_id))
    else:
        st.error("❌ Please enter a review before submitting!")
