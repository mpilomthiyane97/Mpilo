from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from tools.weather_tool import get_weather
# from tools.news_tool import get_news
# from tools.plan_tool import plan_day
import os
from dotenv import load_dotenv

load_dotenv()  # make sure this is called first

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY  # explicitly pass it
)

tools = [get_weather]

agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent(city: str):
    input_text = f"suggest an outfit the user should wear for {city}'s weather using current weather."
    return agent_executor.invoke(input_text)
