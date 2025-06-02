import os
import sys
from typing import List, Dict, Any
import logging

# Import AutoGen components
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Import our tools
from tools.weather_tool import get_weather
from tools.calculator_tool import calculate
from tools.currency_tool import convert_currency
from tools.tool_manager import ToolManager

# Configure logging - file only for detailed logs
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/agent.log"),
    ]
)
logger = logging.getLogger("MultiToolAgent")

# Suppress unnecessary AutoGen logs
logging.getLogger('autogen').setLevel(logging.WARNING)
logging.getLogger('autogen_agentchat').setLevel(logging.WARNING)

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Initialize the tool manager
tool_manager = ToolManager()

# Register tools with descriptions
tool_manager.register_tool(
    "get_weather", 
    get_weather, 
    "Get current weather information for a specified city"
)

tool_manager.register_tool(
    "calculate", 
    calculate, 
    "Evaluate a mathematical expression and return the result"
)

tool_manager.register_tool(
    "convert_currency", 
    convert_currency, 
    "Convert an amount from one currency to another using exchange rates"
)

# Create wrapper functions that log reasoning through the tool manager
def weather_with_reasoning(city: str, reasoning: str) -> str:
    """Wrapper for weather tool that logs reasoning"""
    return tool_manager.execute_tool("get_weather", reasoning, city=city)

def calculate_with_reasoning(expression: str, reasoning: str) -> str:
    """Wrapper for calculator tool that logs reasoning"""
    return tool_manager.execute_tool("calculate", reasoning, expression=expression)

def currency_with_reasoning(amount: float, from_currency: str, to_currency: str, reasoning: str) -> str:
    """Wrapper for currency tool that logs reasoning"""
    return tool_manager.execute_tool(
        "convert_currency", 
        reasoning, 
        amount=amount, 
        from_currency=from_currency, 
        to_currency=to_currency
    )

# Define the model client using GPT-4o with the OpenAI API key
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
)

# Create the system message with tool descriptions
available_tools = tool_manager.get_available_tools()
tool_descriptions = "\n".join([f"- {name}: {desc}" for name, desc in available_tools.items()])

# Custom print function for cleaner output
def pretty_print(message, role="assistant"):
    """Print messages in a more readable format"""
    if role == "assistant":
        prefix = "\n💬 Assistant: "
    elif role == "system":
        prefix = "\n🔔 System: "
    elif role == "user":
        prefix = "\n👤 User: "
    else:
        prefix = "\n💬 "
    
    print(f"{prefix}{message}\n")
    sys.stdout.flush()

system_message = f"""
You are a helpful assistant with access to multiple tools. You can reason step-by-step to select the most appropriate tool for a given task.

Available tools:
{tool_descriptions}

When a user asks a question, follow this process:
1. Think step-by-step about what the user is asking.
2. Decide which tool would be most appropriate to use, if any.
3. Explain your reasoning for selecting a particular tool.
4. Call the appropriate tool with the necessary parameters.
5. Once you have the tool's output, explain what it means and provide any additional context.

Always explain your reasoning out loud before and after using a tool. Be transparent about your decision-making process.

Keep your responses concise and focused. Avoid unnecessary verbosity.
"""

# Initialize the assistant agent with tool use and reasoning capabilities
assistant = AssistantAgent(
    name="multi_tool_assistant",
    model_client=model_client,
    tools=[
        weather_with_reasoning,
        calculate_with_reasoning,
        currency_with_reasoning
    ],
    system_message=system_message,
    reflect_on_tool_use=True,
    model_client_stream=True
)

def get_tool_usage_summary() -> Dict[str, Any]:
    """
    Get a summary of tool usage statistics and execution history.
    
    Returns:
        Dict[str, Any]: Summary of tool usage
    """
    return {
        "usage_stats": tool_manager.get_usage_stats(),
        "execution_count": len(tool_manager.get_execution_history()),
        "last_executions": tool_manager.get_execution_history()[-5:] if tool_manager.get_execution_history() else []
    }

def export_execution_history(file_path: str = "logs/execution_history.json") -> None:
    """
    Export the full execution history to a JSON file.
    
    Args:
        file_path (str): Path to save the JSON file
    """
    tool_manager.export_execution_history(file_path)
    logger.info(f"Exported execution history to {file_path}")
