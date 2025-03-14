
# Appendix

## Project Overview
This repository contains the source code for a **Luxury Hotel Management System** built using **Streamlit**. The project provides an interactive dashboard for users to book stays, submit reviews, and access premium hotel analytics.

## File Structure
- `auth.py` - Handles user authentication, login, and session management.
- `home.py` - Main homepage for logged-in users, displaying services, dashboards, and navigation options.
- `pages/Hotel_Booking_form.py` - Booking interface for guests.
- `pages/Customer_Review_submission.py` - Customer review submission page.
- `pages/BookingsInfo_Dashboard.py` - Dashboard displaying hotel bookings.
- `pages/DiningInfo_Dashboard.py` - Dashboard for dining and restaurant insights.
- `pages/Reviews_dashboard.py` - Dashboard summarizing customer feedback and ratings.

## Setup Instructions
### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/luxury-hotel-management.git
   cd luxury-hotel-management
   ```
2. Install dependencies:
   ```bash
   pip install streamlit
   ```

### **Running the Application**
1. Start the authentication system:
   ```bash
   streamlit run auth.py
   ```
2. Open a new terminal and run the main home page:
   ```bash
   streamlit run home.py
   ```
3. Access the web app in your browser at `http://localhost:8501`

## Authentication Flow
- The `auth.py` file verifies users before granting access.
- Once authenticated, users are redirected to `home.py`.
- If a user is not logged in, they are prompted to sign in first.

### Output Images
![Screenshot 2025-03-14 182044](https://github.com/user-attachments/assets/e748feeb-2a51-478f-858c-a5ad49f99999)
![Screenshot 2025-03-14 182058](https://github.com/user-attachments/assets/32d29ca9-645b-41b7-86e3-b538f629a088)
![Screenshot 2025-03-14 183313](https://github.com/user-attachments/assets/54ab6c51-2fbd-447b-819f-c92a07746041)
![Screenshot 2025-03-14 183417](https://github.com/user-attachments/assets/fc494ef7-9df0-4d19-8c45-e8127232c949)
![Screenshot 2025-03-14 183323](https://github.com/user-attachments/assets/e7eccca3-f769-49f7-9d59-ed0a5f6d6982)



