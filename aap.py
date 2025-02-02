import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("data.csv")

# Select relevant features and target variable
features = ["Gender", "Blood Pressure", "BMI Category", "Age"]
target = "Sleep Disorder"

# Drop rows with missing values
data = data.dropna(subset=features + [target])

# Map Blood Pressure values
bp_mapping = {
    "Low": lambda x: x < 120/80,
    "Normal": lambda x: x == 120/80,
    "High": lambda x: x > 120/80
}

def map_bp(value):
    systolic, diastolic = map(int, value.split("/"))
    bp_value = systolic / diastolic
    for category, condition in bp_mapping.items():
        if condition(bp_value):
            return category
    return "Normal"

data["Blood Pressure"] = data["Blood Pressure"].apply(map_bp)

# Encode categorical variables
label_encoders = {}
for col in features + [target]:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Train model
X = data[features]
y = data[target]
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X, y)

def predict_sleep_disorder(gender, blood_pressure, bmi_category, age, sleep_duration, sleep_quality, daytime_sleepiness):
    user_data = pd.DataFrame({
        "Gender": [gender],
        "Blood Pressure": [blood_pressure],
        "BMI Category": [bmi_category],
        "Age": [age]
    })
    
    # Handle unseen labels
    for col in features:
        if col in label_encoders:
            known_classes = set(label_encoders[col].classes_)
            user_data[col] = user_data[col].apply(lambda x: x if x in known_classes else known_classes.pop())
            user_data[col] = label_encoders[col].transform(user_data[col])
    
    prediction = model.predict(user_data)
    disorder = label_encoders[target].inverse_transform(prediction)[0]
    
    # Conditional mapping based on additional sleep-related questions
    if sleep_duration < 5 and sleep_quality == "Poor":
        disorder = "Insomnia"
    elif daytime_sleepiness == "High" and sleep_duration > 8:
        disorder = "Narcolepsy"
    elif sleep_quality == "Interrupted" and (blood_pressure == "High" or bmi_category=="Obese") :
        disorder = "Sleep Apnea"
    elif sleep_duration > 6 or sleep_quality == "Good":
        disorder = "No Disorder"
    
    disorder_descriptions = {
        "Insomnia": "A disorder that makes it hard to fall or stay asleep.",
        "Sleep Apnea": "A condition where breathing repeatedly stops and starts during sleep.",
        "No Disorder":"You have a healthy Sleep Pattern",
        "Narcolepsy": "A chronic sleep disorder characterized by overwhelming daytime drowsiness."
    }
    return disorder, disorder_descriptions.get(disorder, "No description available.")

# Streamlit UI
st.title("Sleep Disorder Prediction")
gender = st.selectbox("Gender", label_encoders["Gender"].classes_)
blood_pressure = st.selectbox("Blood Pressure", ["Low", "Normal", "High"])
bmi_category = st.selectbox("BMI Category", label_encoders["BMI Category"].classes_)
age = st.number_input("Age", min_value=1, max_value=100, step=1)
sleep_duration = st.number_input("Average Sleep Duration (hours)", min_value=1, max_value=12, step=1)
sleep_quality = st.selectbox("Quality of Sleep", ["Good", "Average", "Poor", "Interrupted"])
daytime_sleepiness = st.selectbox("Daytime Sleepiness Level", ["Low", "Moderate", "High"])

if st.button("Predict"):
    prediction, description = predict_sleep_disorder(gender, blood_pressure, bmi_category, age, sleep_duration, sleep_quality, daytime_sleepiness)
    st.write(f"Predicted Sleep Disorder: {prediction}")
    st.write(f"Description: {description}")


