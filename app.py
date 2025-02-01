import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from sleep import sleep_questionnaire  # Import sleep questionnaire from sleep.py
from data import analyze_sleep  # Import sleep analysis function from data.py

# Load sleep health rules
rules_path = "rules.json"
with open(rules_path, "r") as file:
    rules = json.load(file)

# Define a mapping for 'wake_ups' values to numeric values
wake_up_mapping = {
    "Never": 0,       # "Never" means no wake-ups
    "Sometimes": 1,   # "Sometimes" means a few wake-ups
    "Frequently": 2   # "Frequently" means many wake-ups
}



# Get user input from sleep.py
user_data = sleep_questionnaire()

# Process user data only if available
if user_data:
    try:
        # Ensure correct types for the data being processed
        user_data_processed = {
            "sleep_duration": float(user_data["sleep_hours"]),  # Ensure sleep duration is a float
            "screen_time": 3 if user_data["screen_time"] == "Yes" else 0,  # Convert Yes/No to numeric
            "caffeine_after_6pm": True if user_data["caffeine"] == "Yes" else False,
            
            # Handle 'wake_ups' using the defined mapping
            "wake_ups": wake_up_mapping.get(user_data["wake_ups"], 0),  # Default to 0 if not mapped
            
            # Keep stress as a string value, no need to convert it to a numeric value
            "stress": user_data["stress"]
        }

        # Debug output for processed user data
        st.write(f"Processed User Data: {user_data_processed}")
        
        # Pass the correctly formatted dictionary to analyze_sleep
        insights = analyze_sleep(user_data_processed)
        
        # Recommended sleep values
        ideal_values = {
            "Sleep Duration": 7.5,  # Recommended 7-9 hours
            "Screen Time": 1,  # Should be <2 hours before bed
            "Wake-ups": 1,  # Ideally fewer wake-ups
            "Stress Level": 0  # Low stress is better (use string representation for stress)
        }

        # Process user data for visualization, but handle "stress" separately
        user_values = {
            "Sleep Duration": user_data_processed["sleep_duration"],
            "Screen Time": user_data_processed["screen_time"],
            "Wake-ups": user_data_processed["wake_ups"],
            "Stress Level": user_data_processed["stress"]  # Keep stress as a string for display
        }

        # Ensure all other values are numeric for plotting (stress will be handled separately)
        user_scores = [float(value) if isinstance(value, (int, float)) else 0 for value in user_values.values()]
        ideal_scores = [float(value) if isinstance(value, (int, float)) else 0 for value in ideal_values.values()]

        # --- Visualization Section ---
        try:
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

            # Description for Bar chart
            st.write("""
                This bar chart compares your actual sleep data against the recommended ideal values. 
                - **Sleep Duration**: Ideally 7-9 hours of sleep each night.
                - **Screen Time**: The goal is to limit screen time to less than 2 hours before bedtime.
                - **Wake-ups**: Fewer wake-ups during sleep are better for restfulness.
                - **Stress Level**: Lower stress leads to better sleep quality.
            """)

            # Pie chart: Stress Level Distribution (High vs Low)
            st.subheader("Stress Level Distribution")
            stress_count = {"High": 0, "Low": 0}

            # Handling different cases for stress level to avoid errors
            if user_data_processed["stress"] == "high":
                stress_count["High"] += 1
            elif user_data_processed["stress"] == "low":
                stress_count["Low"] += 1
            else:
                st.error(f"Unexpected stress level: {user_data_processed['stress']}")

            if sum(stress_count.values()) > 0:  # Only show pie chart if there is valid data
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(stress_count.values(), labels=stress_count.keys(), autopct='%1.1f%%', startangle=90, colors=["#ff9999", "#66b3ff"])
                ax.set_title("Stress Level Distribution")
                st.pyplot(fig)
                st.write("The pie chart illustrates the distribution of your stress levels: High vs Low.")

            else:
                st.write("No valid stress level data available.")

            # Scatter Plot: Screen Time vs Sleep Duration
            st.subheader("Screen Time vs Sleep Duration")
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(user_data_processed["screen_time"], user_data_processed["sleep_duration"], color='purple', s=100, edgecolors="black")
            ax.set_xlabel("Screen Time (hours)")
            ax.set_ylabel("Sleep Duration (hours)")
            ax.set_title("Screen Time vs Sleep Duration")
            st.pyplot(fig)

            # Description for Scatter Plot
            st.write("""
                This scatter plot visualizes the relationship between screen time and sleep duration. 
                - **Screen Time**: Hours spent on screens before bed.
                - **Sleep Duration**: The total hours you sleep each night.
                Typically, higher screen time is associated with reduced sleep duration.
            """)

            # Heatmap: Correlation between Screen Time, Wake-ups, and Caffeine After 6 PM
            st.subheader("Correlation Heatmap")
            try:
                data = np.array([
                    [user_data_processed["screen_time"], user_data_processed["wake_ups"], int(user_data_processed["caffeine_after_6pm"])]
                ])
                corr_matrix = np.corrcoef(data.T)

                fig, ax = plt.subplots(figsize=(6, 5))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', xticklabels=["Screen Time", "Wake-ups", "Caffeine After 6 PM"],
                            yticklabels=["Screen Time", "Wake-ups", "Caffeine After 6 PM"], cbar=True, ax=ax)
                ax.set_title("Correlation Heatmap")
                st.pyplot(fig)

                # Description for Heatmap
                st.write("""
                    This heatmap shows the correlation between screen time, wake-ups, and caffeine consumption after 6 PM. 
                    - **Screen Time**: Increased screen time can affect your sleep quality.
                    - **Wake-ups**: Frequent wake-ups during sleep impact the overall quality of rest.
                    - **Caffeine After 6 PM**: Consuming caffeine late in the day can disrupt your sleep.
                """)
                

            except Exception as e:
                st.error(f"Error while generating heatmap: {e}")
                print(f"Error while generating heatmap: {e}")

            # Display insights
            st.subheader("Personalized Insights")
            for insight in insights:
                st.write(f"- {insight}")

        except Exception as e:
            st.error(f"An error occurred in the visualization section: {e}")
            print(f"An error occurred in the visualization section: {e}")

    except ValueError as e:
        st.error(f"Invalid data: {e}")
        print(f"Invalid data: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

else:
    st.error("No user data received.")





