import streamlit as st

# Set up page title and layout
st.set_page_config(page_title="Luxury Hotel | Home", layout="wide")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Apply CSS styles for full centering
st.markdown("""
    <style>
        /* Center everything */
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            justify-content: center;
            margin-top: 20px;
        }

        /* Background Image */
        .stApp {
            background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                        url('https://source.unsplash.com/1600x900/?luxury,resort') no-repeat center fixed;
            background-size: cover;
        }

        /* Title Styling */
        .title {
            color: #2F4F6F;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 1px 1px 4px #FFFFFF;
        }

        /* Subtitle Styling */
        .subtitle {
            color: #5A5A5A;
            font-size: 20px;
            margin-bottom: 30px;
            text-shadow: 1px 1px 3px #FFFFFF;
        }

        /* Button Container */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        /* Stylish Buttons */
        .stButton>button {
            background: linear-gradient(to right, #FFD700, #FFA500);
            color: white;
            border: none;
            padding: 14px 24px;
            border-radius: 14px;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
        }

        .stButton>button:hover {
            background: linear-gradient(to right, #FFA500, #FF7F50);
            transform: scale(1.08);
        }
    </style>
""", unsafe_allow_html=True)

# Ensure user is logged in
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("⚠️ Please log in first!")
    st.switch_page("auth.py")  # Redirect to login if not logged in

# Center Container
st.markdown('<div class="center-container">', unsafe_allow_html=True)

# Welcome Section
st.markdown("<h1 class='title'>🏨 Welcome to Luxury Hotel</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>Hello, <strong>{st.session_state['user']['name']}</strong>! Relax and explore our premium hotel services.</p>", unsafe_allow_html=True)

# 📌 Centered Main Services Section
st.subheader("🛎️ Main Services")
st.markdown('<div class="button-container">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🛎️ Book a Stay"):
        st.switch_page("pages/Hotel_Booking_form.py")

with col2:
    if st.button("📝 Submit a Review"):
        st.switch_page("pages/Customer_Review_submission.py")

st.markdown('</div>', unsafe_allow_html=True)

# 📌 Centered Premium Dashboards Section
st.subheader("📊 Premium Dashboards")
st.markdown('<div class="button-container">', unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    if st.button("📅 View Booking Dashboard"):
        st.switch_page("pages/BookingsInfo_Dashboard.py")

with col4:
    if st.button("🍽️ Dining & Restaurant Insights"):
        st.switch_page("pages/DiningInfo_Dashboard.py")

with col5:
    if st.button("💬 Customer Feedback & Ratings"):
        st.switch_page("pages/Reviews_dashboard.py")

st.markdown('</div>', unsafe_allow_html=True)

# Footer message
st.markdown("<p class='subtitle'>✨ Enjoy a luxurious experience at our 5-star hotel! ✨</p>", unsafe_allow_html=True)

# Close the center container
st.markdown('</div>', unsafe_allow_html=True)
