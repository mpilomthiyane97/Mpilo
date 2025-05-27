from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.weather_tool import get_weather  # Use the plain function

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
)

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
    model_client_stream=False,
)


async def chat_with_assistant(user_input: str) -> str:
    result = await assistant.run(task=user_input)
    await model_client.close()

    # print("\n🔍 Raw assistant output:", result)

    # Extract the latest message from the assistant
    if hasattr(result, "messages") and result.messages:
        for msg in reversed(result.messages):
            if msg.source == "weather_assistant" and hasattr(msg, "content"):
                return msg.content

    return "Sorry, I couldn't process your request."


