import streamlit as st

def sleep_questionnaire():
    st.title("Sleepology - Sleep Analyzer")
    st.write("Compare your sleep habits with recommended guidelines.")
    # Basic Information
    st.header("Basic Information")
    age = st.number_input("Age", min_value=0, max_value=100, value=0)
    gender = st.radio("Gender", ["Male", "Female", "Other"], index=None)
    occupation = st.text_input("Occupation")
    
    # Sleep Schedule
    st.header("Sleep Schedule & Duration")
    bedtime = st.selectbox("What time do you usually go to bed?", ["Before 9 PM", "9-10 PM", "10-11 PM", "11 PM-12 AM", "After 12 AM"])
    waketime = st.selectbox("What time do you usually wake up?", ["Before 5 AM", "5-6 AM", "6-7 AM", "7-8 AM", "After 8 AM"])
    sleep_hours = st.slider("How many hours of sleep do you get on average?", 0, 10, 0)
    consistent_schedule = st.radio("Do you have a consistent sleep schedule?", ["Yes", "No", "Somewhat"], index=None)
    
    # Sleep Quality & Disturbances
    st.header("Sleep Quality & Disturbances")
    sleep_quality = st.slider("Rate your overall sleep quality", 1, 10, 0)
    wake_ups = st.selectbox("How many times do you wake up at night?", ["Never", "Sometimes", "Frequently"])
    fall_asleep_time = st.slider("How long does it take to fall asleep (minutes)?", 0, 60, 0)
    disturbances = st.selectbox("Do you experience any of these during sleep?", ["Snoring", "Restless sleep", "Nightmares", "Sleep talking", "Sleepwalking", "Teeth grinding", "None"])
    wake_refreshed = st.radio("How often do you wake up feeling refreshed?", ["Every day", "Most days", "Some days", "Rarely", "Never"], index=None)
    
    # Lifestyle & Sleep Hygiene
    st.header("Lifestyle & Sleep Hygiene")
    caffeine = st.radio("Do you consume caffeine?", ["Yes", "No"], index=None)
    caffeine_time = None
    if caffeine == "Yes":
        caffeine_time = st.selectbox("Last caffeine intake before bed?", ["Less than 1 hour", "1-2 hours", "More than 3 hours"])
    alcohol = st.radio("Do you consume alcohol before bed?", ["Yes", "No"], index=None)
    screen_time = st.radio("Do you use electronic devices before sleeping?", ["Yes", "No"], index=None)
    exercise = st.radio("When do you exercise?", ["Morning workout", "Afternoon workout", "Evening workout", "No workout"], index=None)
    exercise_freq = st.slider("Days per week you exercise", 0, 7, 0)
    
    # Sleep Environment
    st.header("Sleep Environment")
    comfort_level = st.slider("How comfortable is your sleep environment?", 1, 10, 0)
    sleep_disturbances = st.selectbox("What factors disturb your sleep?", ["Noise", "Light", "Temperature", "Partner’s movement", "Pets", "None"])
    lights_on = st.radio("Do you sleep with the lights on?", ["Yes", "No", "Sometimes"], index=None)
    sleep_aids = st.radio("Do you use sleep aids?", ["Yes", "No", "Sometimes"], index=None)
    
    # Health & Sleep Impact
    st.header("Mental & Physical Health")
    health_issues = st.selectbox("Do you have any of these health conditions?", ["Insomnia", "Sleep apnea", "Anxiety", "Depression", "Chronic pain", "High blood pressure", "Diabetes", "None"])
    sleep_medication = st.radio("Do you take sleep medication?", ["Yes", "No"], index=None)
    stress_level = st.slider("How stressed do you feel before bedtime?", 1, 10, 0)
    daytime_sleepiness = st.radio("Do you experience excessive daytime sleepiness?", ["Yes", "No"], index=None)
    morning_headache = st.radio("Do you have frequent morning headaches?", ["Yes", "No"], index=None)
    medical_treatment = st.radio("Are you undergoing any medical treatment affecting sleep?", ["Yes", "No"], index=None)
    
    # Sleep Goals
    st.header("Sleep Goals")
    sleep_goals = st.multiselect("What are your sleep improvement goals?", ["Improve sleep quality", "Fall asleep faster", "Wake up refreshed", "Reduce daytime sleepiness", "Reduce snoring", "Reduce nightmares"])
    
    # Submit Button
    if st.button("Submit & Analyze"):
        st.success("Your data has been recorded. Generating analysis...")
        
        return {
            "age": age,
            "gender": gender,
            "sleep_hours": sleep_hours,
            "screen_time": screen_time,
            "wake_ups": wake_ups,
            "stress": stress_level,
            "caffeine": caffeine,
            "caffeine_time": caffeine_time,
            "sleep_quality": sleep_quality
        }
    return None

if __name__ == "_main_":
    user_data = sleep_questionnaire()