import logging
import os
from typing import Callable, Dict, List, Any
import json
import time

# Configure logging - file only for detailed logs
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/tool_usage.log"),
    ]
)

# Create a separate console logger for user-facing information
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(message)s'))

console_logger = logging.getLogger("console")
console_logger.addHandler(console_handler)
console_logger.propagate = False  # Prevent double logging

class ToolManager:
    """
    Manages multiple tools, handles tool selection, and logs tool usage and reasoning.
    """
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_descriptions: Dict[str, str] = {}
        self.usage_stats: Dict[str, int] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("ToolManager")
    
    def register_tool(self, name: str, tool_func: Callable, description: str):
        """
        Register a tool with the manager.
        
        Args:
            name (str): Name of the tool
            tool_func (Callable): The tool function
            description (str): Description of what the tool does
        """
        self.tools[name] = tool_func
        self.tool_descriptions[name] = description
        self.usage_stats[name] = 0
        self.logger.info(f"Registered tool: {name}")
    
    def get_available_tools(self) -> Dict[str, str]:
        """
        Get all available tools and their descriptions.
        
        Returns:
            Dict[str, str]: Dictionary of tool names and descriptions
        """
        return self.tool_descriptions
    
    def execute_tool(self, tool_name: str, reasoning: str, **kwargs) -> str:
        """
        Execute a tool and log the execution details.
        
        Args:
            tool_name (str): Name of the tool to execute
            reasoning (str): The reasoning for selecting this tool
            **kwargs: Arguments to pass to the tool
            
        Returns:
            str: Result from the tool execution
        """
        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
            self.logger.error(error_msg)
            return error_msg
        
        # Log the tool selection reasoning to file only
        self.logger.info(f"Tool selection reasoning: {reasoning}")
        # Print a user-friendly message to console
        tool_emoji = "🌤️" if "weather" in tool_name else "🧮" if "calculate" in tool_name else "💱" if "currency" in tool_name else "🛠️"
        tool_display_name = tool_name.replace('_', ' ').title()
        console_logger.info(f"\n{tool_emoji} Using {tool_display_name}")
        console_logger.info(f"💭 Reasoning: {reasoning}")
        
        # Execute the tool and time its execution
        start_time = time.time()
        try:
            result = self.tools[tool_name](**kwargs)
            execution_time = time.time() - start_time
            
            # Update usage statistics
            self.usage_stats[tool_name] += 1
            
            # Record execution details
            execution_record = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "tool": tool_name,
                "reasoning": reasoning,
                "arguments": kwargs,
                "result": result,
                "execution_time": execution_time
            }
            self.execution_history.append(execution_record)
            
            # Log the execution details to file
            self.logger.info(f"Executed {tool_name} with args: {json.dumps(kwargs)}")
            self.logger.info(f"Result: {result}")
            self.logger.info(f"Execution time: {execution_time:.4f} seconds")
            
            # Print user-friendly output to console
            console_logger.info(f"📊 Result: {result}\n")
            
            return result
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            self.logger.error(error_msg)
            
            # Record execution failure
            execution_record = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "tool": tool_name,
                "reasoning": reasoning,
                "arguments": kwargs,
                "error": str(e),
                "execution_time": time.time() - start_time
            }
            self.execution_history.append(execution_record)
            
            return error_msg
    
    def get_usage_stats(self) -> Dict[str, int]:
        """
        Get usage statistics for all tools.
        
        Returns:
            Dict[str, int]: Dictionary of tool names and usage counts
        """
        return self.usage_stats
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """
        Get the full execution history.
        
        Returns:
            List[Dict[str, Any]]: List of execution records
        """
        return self.execution_history
    
    def export_execution_history(self, file_path: str) -> None:
        """
        Export the execution history to a JSON file.
        
        Args:
            file_path (str): Path to save the JSON file
        """
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path) or "logs", exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(self.execution_history, f, indent=2)
        self.logger.info(f"Exported execution history to {file_path}")
        console_logger.info(f"\n📝 Execution history saved to {file_path}\n")
