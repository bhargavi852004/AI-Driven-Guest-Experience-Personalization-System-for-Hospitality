
# Dish Recommendation System with Email Notification

## Overview
This project features an AI-powered dish recommendation system that utilizes XGBoost for predictive analysis based on customer data. Additionally, a user-friendly interface is developed using Streamlit, enabling customers to receive booking details and exclusive coupon codes via email.

## Features
- **Dish Recommendation**: Predicts and recommends dishes based on customer preferences using an XGBoost model.
- **Streamlit Interface**: User-friendly UI for customer interaction.
- **Email Notification**: Sends booking details and coupon codes to customers via email.

## Technology Stack
- **Machine Learning Model**: XGBoost for dish prediction.
- **Web Interface**: Streamlit for interactive UI.
- **Email Integration**: SMTP for sending booking details and coupon codes.
- **MongoDb**: For DataBase

## Installation & Setup
### Prerequisites
Ensure you have:
- Python (>=3.8)
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### Running the Project
 1. Train the XGBoost model (if needed):
   ```sh
   python xg_boost_model.py
   ```
2. Run the Streamlit app:
   ```sh
   streamlit run Interface.py
   ```

### Output Samples
#### User Interface of the Streamlit App
![User_Interface](https://github.com/user-attachments/assets/deee396c-09da-45ed-8719-9d5f8843f041)
#### Displaying of Booking Information at User Interface
![Booking Info](https://github.com/user-attachments/assets/2f3177b2-b6f9-4361-9635-7a74274deeef)
#### A Confirmation email that has been automated which contains information about Booking and Coupon Code
![Email_confirmation](https://github.com/user-attachments/assets/a118c6d3-ebee-4d5e-9bd7-a86122b3761f)
#### DataBase containing the information of new Booking
![New_Data DB](https://github.com/user-attachments/assets/2f2471ca-dda3-4780-93af-ede7dde14a58)



