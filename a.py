import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier  # Or any other classifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
data = pd.read_csv(r"C:\Users\Thrishaa J\Downloads\Sleep_health_and_lifestyle_dataset.csv")

# Clean the data and preprocess
data_filtered = data[data['Sleep Disorder'].notna()]  # Remove rows with missing target
categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Blood Pressure']
data_train = pd.get_dummies(data_filtered, columns=categorical_cols, drop_first=True)
le = LabelEncoder()
data_train['Sleep Disorder'] = le.fit_transform(data_train['Sleep Disorder'])

# Prepare features and target variable
X = data_train.drop('Sleep Disorder', axis=1)
y = data_train['Sleep Disorder']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Predict on test data
y_pred_test = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred_test)
classification_report_str = classification_report(y_test, y_pred_test)
confusion_matrix_str = confusion_matrix(y_test, y_pred_test)

# Streamlit UI
st.title("Sleep Disorder Prediction and Insights")

# Show accuracy and metrics
st.subheader("Model Accuracy")
st.write(f"Accuracy on the test set: {accuracy}")
st.write("### Classification Report")
st.write(classification_report_str)
st.write("### Confusion Matrix")
st.write(confusion_matrix_str)

# Predict on new data (for prediction insights)
# Assume you have data to predict (data_predict)
data_predict = data[data['Sleep Disorder'].isnull()].copy()  # Sample prediction data
data_predict = pd.get_dummies(data_predict, columns=categorical_cols, drop_first=True)
# Ensure columns match the training set
for col in X_train.columns:
    if col not in data_predict.columns:
        data_predict[col] = 0
data_predict = data_predict[X_train.columns]

data_predict_scaled = scaler.transform(data_predict)
y_pred_predict = model.predict(data_predict_scaled)
predicted_sleep_disorder = le.inverse_transform(y_pred_predict)  # Decode back to original labels

# Add predicted results back to the dataframe
data_predict['Predicted_Sleep_Disorder'] = predicted_sleep_disorder
st.write("### Predicted Sleep Disorder for Individuals")
st.write(data_predict[['Person ID', 'Predicted_Sleep_Disorder']])

# Optionally save the predictions
# data_predict.to_csv('predicted_sleep_disorders.csv', index=False)

# Merge predictions back into the original data
data = pd.merge(data, data_predict[['Person ID', 'Predicted_Sleep_Disorder']], on='Person ID', how='left')

# Fill missing 'Sleep Disorder' values with the predictions
data['Sleep Disorder'].fillna(data['Predicted_Sleep_Disorder'], inplace=True)

# Display updated data info
st.write("### Updated Data with Predictions")
st.write(data.info())

# Show Insights: Sleep Health Insights Based on Predictions
st.subheader("Personalized Sleep Insights")
user_data_processed = {
    # Example features for insights
    "sleep_duration": 7.5,  # Example value
    "screen_time": 2,  # Example value
    "wake_ups": 1,  # Example value
    "stress": "low"  # Example value
}

# Define ideal values for comparison
ideal_values = {
    "Sleep Duration": 7.5,
    "Screen Time": 1,
    "Wake-ups": 1,
    "Stress Level": 0  # Low stress is best
}

# Visualization for Sleep Insights
user_values = {
    "Sleep Duration": user_data_processed["sleep_duration"],
    "Screen Time": user_data_processed["screen_time"],
    "Wake-ups": user_data_processed["wake_ups"],
    "Stress Level": user_data_processed["stress"]
}

user_scores = [float(value) if isinstance(value, (int, float)) else 0 for value in user_values.values()]
ideal_scores = [float(value) if isinstance(value, (int, float)) else 0 for value in ideal_values.values()]

# Bar chart: User Data vs Ideal Requirements
st.subheader("Comparison of Your Sleep Data vs Ideal Recommendations")
labels = list(user_values.keys())
x = np.arange(len(labels))

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - 0.2, user_scores, width=0.4, label="User Data", color='skyblue')
ax.bar(x + 0.2, ideal_scores, width=0.4, label="Ideal Values", color='lightgreen')
ax.axhline(0, color="black", linestyle="--")
ax.set_xticks(ticks=x)
ax.set_xticklabels(labels, rotation=20)
ax.set_ylabel("Score / Impact")
ax.set_title("Sleep Analysis: User Data vs Ideal Sleep Recommendations")
ax.legend()
st.pyplot(fig)

# Show additional insights (e.g., prediction of Sleep Disorder)
st.write("### Sleep Disorder Prediction Insights")
# For instance, show distribution of predictions across genders or other factors
st.subheader("Predicted Sleep Disorder Distribution")
sns.countplot(x='Predicted_Sleep_Disorder', data=data, palette="Blues")
st.pyplot()

# Final update on the dataset
st.write("### Final Dataset with Predicted Sleep Disorder")
st.write(data.head())
