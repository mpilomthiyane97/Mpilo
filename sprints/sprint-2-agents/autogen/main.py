import asyncio
from agent import chat_with_assistant

if __name__ == "__main__":
    city = input("📍 Enter your city: ").strip()
    prompt = f"Suggest an outfit the user should wear for {city}'s weather using current weather."
    response = asyncio.run(chat_with_assistant(prompt))
    print(response)
