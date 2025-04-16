# AI-Driven Guest Experience Personalization System for Hospitality

## Project Overview
This project develops an **AI-driven system** to enhance hospitality guest experiences using **Large Language Models (LLMs)** like OpenAI GPT and Meta LLaMA. The system analyzes guest feedback, monitors sentiment trends, and dynamically personalizes recommendations for dining, activities, and amenities. By integrating real-time alerts for service teams, the solution ensures adaptive, tailored experiences that evolve with guest preferences during their stay.

## Key Outcomes
- **Personalized recommendations** for dining, activities, and amenities based on guest behavior analysis.
- **Real-time sentiment monitoring** to proactively address guest feedback.
- **Increased guest satisfaction** through dynamic personalization.
- **Automated alerts for staff** to resolve issues and optimize service delivery.

---
## Repository Structure & Milestones
The project is structured into **four milestones**, each building upon the previous one to develop a robust AI-powered guest experience system.

### **Milestone 1: Building & Evaluating a Machine Learning Model for Favorite Dish Prediction**
**Objective:** Predict the favorite dish of a customer based on their dining preferences and behavior.

**Key Steps:**
1. **Data Preparation** – Loaded the dataset, split it into feature extraction, training, and testing sets based on time-based logic.
2. **Feature Engineering** – Computed customer-level and cuisine-level features.
3. **Data Integration** – Merged engineered features into the training and testing datasets.
4. **Encoding & Model Training** – Applied one-hot encoding for categorical data and trained an **XGBoost Classifier** for dish prediction.
5. **Model Evaluation** – Assessed model performance using accuracy, log loss, and feature importance analysis.

✅ **Outcome:** Developed an XGBoost model for predicting a guest’s favorite dish with **0.18 accuracy**.

---

### **Milestone 2: Guest Preference Modeling & Personalized Recommendation System along with Booking UI**
**Objective:** Develop a recommendation engine to suggest personalized amenities and activities for guests.

**Key Steps:**
1. Extracted features like frequency of activity participation, preferred times, and past spending patterns.
2. Implemented **User-Based & Item-Based Filtering** to recommend relevant activities based on guest preferences.
3. Used **TF-IDF & Cosine Similarity** to generate activity recommendations based on textual guest preferences.
4. Combined collaborative and content-based approaches for improved accuracy.

✅ **Output:** Built a **Hotel Booking UI with Personalized Recommendations** that adapts to guest preferences and historical behaviors.

---

### **Milestone 3: Real-Time Sentiment Monitoring & Guest Feedback Analysis**
**Objective:** Analyze guest reviews using **Natural Language Processing (NLP)** to monitor sentiment trends and generate real-time alerts.

**Key Steps:**
1. Loaded and cleaned guest feedback data, tokenized text, and removed stopwords and Created Embeddings and Inserting Embeddings and Metadata into index
2. Used Sentiment Analysis for rule-based sentiment scoring  for deeper insights.
3. Tracked sentiment over time, identified top positive/negative topics.
4. Created automated alerts for Manager when negative sentiment was detected for hospitality.

✅ **Outcome:** Implemented **real-time guest sentiment tracking**, allowing proactive issue resolution and improved guest satisfaction.

---
### **Milestone 4: Dashboard Development & Visualization**

**Key Steps:** 
1.  Created interactive dashboards for customer insights, sentiment analysis, and recommendations.
2.  Used Together.AI for graph-based visualization of guest behavior patterns.
3.  Provided real-time tracking of service efficiency and guest satisfaction trends.
4.  Integrated all milestones into a seamless, user-friendly visualization interface.
   
✅ **Output:** created Dashboards for the Hotel Bookings, Hotel Dining Insights, Customer Review Analysis

---
### **pages**
- Integrated all the User Interfaces using auth.py as a login/signup page making it user friendly for all the customer requirements.

###  **Future Enhancements** 
- **Improve Model Accuracy**: Experiment with hyperparameter tuning and deep learning models.
- **Expand Sentiment Monitoring**: Integrate audio sentiment analysis from voice feedback.
- **Enhance Chatbot Capabilities**: Include multi-language support and voice-based interactions.
- **Deploy as a SaaS Solution**: Develop an API for seamless hospitality industry integration.


---
**🚀 AI-Driven Guest Experience Personalization System – Redefining Hospitality with AI!**

