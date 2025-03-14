import streamlit as st
from pymongo import MongoClient
import bcrypt

# Connect to MongoDB (Change if using MongoDB Atlas)
MONGO_URI = "mongodb://localhost:27017"  
client = MongoClient(MONGO_URI)
db = client["user_logins"]  # Use the new database for logins
users_collection = db["users"]  # Collection for storing user data

st.set_page_config(page_title="User Authentication", layout="centered")

# Hide the sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Welcome to Hotel")
st.subheader("Login or Signup to continue")

# Function to check if email exists
def check_user(email):
    return users_collection.find_one({"email": email})

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify passwords
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Initialize session state for login
if "user" not in st.session_state:
    st.session_state["user"] = None  

# If user is logged in, redirect to home page
if st.session_state["user"]:
    st.success(f"✅ Logged in as {st.session_state['user']['name']} ({st.session_state['user']['email']})")
    st.switch_page("pages/home.py")  # Redirect immediately

# Selection: Login or Signup
auth_option = st.radio("Select an option:", ["Login", "Signup"])

if auth_option == "Signup":
    st.subheader("Create a New Account")
    name = st.text_input("👤 Full Name")  # Added Name Input
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    confirm_password = st.text_input("🔄 Confirm Password", type="password")

    if st.button("Sign Up"):
        if not name.strip():
            st.error("❌ Name cannot be empty!")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif check_user(email):
            st.warning("⚠️ Email already exists! Try logging in.")
        else:
            hashed_pw = hash_password(password)
            users_collection.insert_one({"name": name, "email": email, "password": hashed_pw})
            st.success("✅ Account created successfully! You can now log in.")

elif auth_option == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        user = check_user(email)
        if user and verify_password(password, user["password"]):
            st.session_state["user"] = {"name": user["name"], "email": email}  # Store name & email in session
            st.success(f"✅ Welcome, {user['name']}! Redirecting...")
            st.rerun()  # Refresh page to apply session state
        else:
            st.error("❌ Invalid email or password!")
