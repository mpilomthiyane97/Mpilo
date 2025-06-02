#Import necessary components to create and run a LangChain agent
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from tools.weather_tool import get_weather  # Custom tool for fetching real-time weather


import os
from dotenv import load_dotenv

# Load environment variables (e.g., OpenAI API key) from .env file
load_dotenv()

# Retrieve OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the language model (LLM) with low temperature for more deterministic output
llm = ChatOpenAI(
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY  # Explicitly pass API key for safety
)

# Register available tools the agent can choose from — here we use a weather tool
tools = [get_weather]

#Initialize the LangChain agent using the ReAct (Reasoning + Acting) pattern
# This allows the LLM to reason step-by-step and decide when/how to use tools
agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Uses tool descriptions to decide which one to use
    verbose=True  # Enables detailed output for tracing agent's reasoning steps
)

# Main function to run the agent with a user-defined city
# Prompts the agent to suggest an outfit based on current weather in the given city
def run_agent(city: str):
    input_text = f"suggest an outfit the user should wear for {city}'s weather using current weather."
    return agent_executor.invoke(input_text)
