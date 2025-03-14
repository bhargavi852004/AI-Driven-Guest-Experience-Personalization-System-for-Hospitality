# Appendix: Milestone 1 - Predicting Favorite Dish Using XGBoost Classifier

## Introduction
In this milestone, we built and evaluated a machine learning model to predict a customer's favorite dish based on their dining preferences and behavior. The model was trained using structured data processing, feature engineering, and an XGBoost classifier.

## Data Preparation
We split the dataset based on order times to ensure proper training and evaluation:
- **Feature Extraction Data (Before Jan 1, 2024)**: Used to calculate customer preferences.
- **Training Data (Jan 1 – Oct 1, 2024)**: Used to train the model.
- **Testing Data (After Oct 1, 2024)**: Used to evaluate the model.

This approach ensures that our model learns from past trends and is tested on future unseen data.

## Feature Engineering
We created meaningful features to improve predictions. For Example:
- **Customer-Level Features:**
  - Total orders per customer
  - Average spending per customer
  - Total quantity of dishes ordered
- **Cuisine-Level Features:**
  - Average price per cuisine
  - Most preferred cuisine
- **Additional Features from Training Data:**
  - Age
  - Duration of stay
  - Check-in day and month
  - Additional behavioral features from past transactions.

## Data Integration
We merged the training and test data with the extracted features and removed columns that could cause data leakage, such as:
- Transaction ID
- Customer ID
- Order time
- Price per dish (to prevent unfair advantage)
- Quantity ordered

## Encoding Categorical Data
We applied:
- **One-Hot Encoding** for categorical variables like preferred cuisine.
- **Label Encoding** for the target variable (dish) to convert it into numerical form.

## Model Training
We trained an **XGBoost Classifier**, which handles missing values well. Key hyperparameters tested:
- Learning Rate: 0.01 to 1
- Max Depth: 1 to 5
- Number of Estimators: 50 to 500
- Objective: Multi-class classification

## Model Evaluation
After training, we tested the model using:
- **Accuracy**: 18% (indicating room for improvement)
- **Log Loss**: Measures prediction confidence.
- **Feature Importance**: Identified the most important factors influencing predictions.

## Conclusion
This milestone helped us build a baseline model for predicting a customer’s favorite dish. Future improvements include refining features, testing other models, and fine-tuning hyperparameters for better accuracy.

