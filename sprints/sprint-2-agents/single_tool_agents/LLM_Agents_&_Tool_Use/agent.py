# agent.py
from tools import get_weather, dress_recommendation

def run_agent(task, location):
    print(f"🧠 Task: {task} for {location}")
    
    # Step 1: Think
    print("\n🤔 Thought: To recommend what to wear, I need to check the current weather.")

    # Step 2: Act → Call get_weather
    print("🔧 Action: get_weather")
    weather = get_weather(location)

    # Step 3: Observe
    print(f"👁️ Observation: {weather}")

    # Step 4: Think again
    print("\n🤔 Thought: Now that I know the weather, I can generate a clothing recommendation.")

    # Step 5: Act → Call dress_recommendation
    print("🔧 Action: dress_recommendation")
    advice = dress_recommendation(weather)

    # Step 6: Final Answer
    print(f"\n✅ Final Answer:\n{advice}")
