import os
from autogen_agentchat.agents import AssistantAgent  # Core assistant agent class
from autogen_ext.models.openai import OpenAIChatCompletionClient  # Wrapper for OpenAI LLMs
from tools.weather_tool import get_weather  # Custom plain function weather tool

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the model client using GPT-4o with the OpenAI API key
# This acts as the language model that powers the assistant
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
)

# 🤖 Initialize the assistant agent with tool use and reasoning capabilities
assistant = AssistantAgent(
    name="weather_assistant",  # Unique name for the agent (optional but good for tracing)
    model_client=model_client,  # Connect the agent to the GPT-4o model client
    tools=[get_weather],  # Register tools the assistant is allowed to use
    system_message="""
You are a helpful assistant reasoning step-by-step.

When a user asks about the weather or what to wear, follow this process:
1. Think step-by-step about what the user is asking.
2. Decide if you need to use the weather tool.
3. Call the get_weather tool with the city name.
4. Once you have the weather info, explain what it means.
5. Suggest an outfit based on temperature and weather conditions.

Always explain your reasoning out loud before and after using the tool.
""",  #Gives the assistant instructions on how to behave and solve the task

    reflect_on_tool_use=True,  #Enables the agent to self-evaluate its tool usage
    model_client_stream=True,  #Enables response streaming for real-time feedback and tracing
)
