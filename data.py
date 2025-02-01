import json

# Load rules from file
with open("rules.json", "r") as file:
    rules = json.load(file)

# Function to analyze sleep data
def analyze_sleep(data):
    recommendations = []
    
    # Sleep duration check
    if data["sleep_duration"] < rules["sleep_duration"]["low"]["threshold"]:
        recommendations.append(rules["sleep_duration"]["low"]["message"])
    elif data["sleep_duration"] > rules["sleep_duration"]["high"]["threshold"]:
        recommendations.append(rules["sleep_duration"]["high"]["message"])

    # Screen time check
    if data["screen_time"] > rules["screen_time"]["limit"]:
        recommendations.append(rules["screen_time"]["message"])

    # Caffeine check
    if data["caffeine_after_6pm"]:
        recommendations.append(rules["caffeine"]["after_6pm"])

    # Wake-ups check
    if data["wake_ups"] > rules["wake_ups"]["threshold"]:
        recommendations.append(rules["wake_ups"]["message"])

    # Stress check
    if data["stress"] == "high":
        recommendations.append(rules["stress"]["high"])

    return recommendations

# Example user input
user_data = {
    "sleep_duration": 5.5,
    "screen_time": 3,
    "caffeine_after_6pm": True,
    "wake_ups": 3,
    "stress": "high"
}
 

# Run analysis
result = analyze_sleep(user_data)
print(result)
