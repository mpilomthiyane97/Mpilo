# main.py
from agent import run_agent

if __name__ == "__main__":
    location = input("📍 Enter your city or location: ")
    task = "What should I wear today?"
    run_agent(task, location)
