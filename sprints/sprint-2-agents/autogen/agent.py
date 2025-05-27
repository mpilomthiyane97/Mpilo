import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.weather_tool import get_weather  # Plain function tool

# Load your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the model client
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
)

# Create the assistant agent
assistant = AssistantAgent(
    name="weather_assistant",
    model_client=model_client,
    tools=[get_weather],
    system_message="""
You are a helpful assistant reasoning step-by-step.

When a user asks about the weather or what to wear, follow this process:
1. Think step-by-step about what the user is asking.
2. Decide if you need to use the weather tool.
3. Call the get_weather tool with the city name.
4. Once you have the weather info, explain what it means.
5. Suggest an outfit based on temperature and weather conditions.

Always explain your reasoning out loud before and after using the tool.
""",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enables streaming + trace output
)