import asyncio
from agent import assistant, model_client
from autogen_agentchat.ui import Console

if __name__ == "__main__":
    async def main():
        city = input("📍 Enter your city: ").strip()
        task = f"Suggest an outfit the user should wear for {city}'s weather using current weather."
        await Console(assistant.run_stream(task=task))
        await model_client.close()

    asyncio.run(main())
