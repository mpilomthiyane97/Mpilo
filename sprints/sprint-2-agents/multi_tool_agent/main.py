import asyncio
import os
import logging
from agent import assistant, model_client, get_tool_usage_summary, export_execution_history, pretty_print
from autogen_agentchat.ui import Console

# Configure logging to reduce verbosity
logging.basicConfig(level=logging.WARNING)
for logger_name in ['httpx', 'autogen', 'autogen_core.events', 'autogen_agentchat']:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

async def main():
    """
    Main function to run the multi-tool agent.
    """
    print("\n" + "=" * 60)
    print("🤖 MULTI-TOOL AGENT WITH AUTOGEN 🤖".center(60))
    print("=" * 60)
    print("\nThis agent can use multiple tools and logs its reasoning process.")
    print("\nAvailable tools:")
    print("  🌤️  Weather - Get current weather for any city")
    print("  🧮  Calculator - Evaluate mathematical expressions")
    print("  💱  Currency - Convert between different currencies")
    print("\n" + "-" * 60)
    
    # Get user input
    user_input = input("\n🔍 What would you like to know? ").strip()
    print(f"\n👤 User: {user_input}\n")
    print("-" * 60 + "\n")
    
    # Run the assistant with the user's task
    await Console(assistant.run_stream(task=user_input))
    
    # Print tool usage summary
    print("\n" + "-" * 60)
    print("\n📊 TOOL USAGE SUMMARY")
    summary = get_tool_usage_summary()
    for tool, count in summary["usage_stats"].items():
        tool_name = tool.replace('_', ' ').title()
        emoji = "🌤️" if "weather" in tool else "🧮" if "calculate" in tool else "💱" if "currency" in tool else "🛠️"
        print(f"  {emoji}  {tool_name}: {count} uses")
    
    # Export execution history
    export_execution_history("logs/execution_history.json")
    
    # Close the model client
    await model_client.close()

if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY environment variable not set.")
        print("    Please set it in the .env file or directly in your environment.")
        print("\n" + "-" * 60)
        exit(1)
    
    try:
        # Run the main function
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n" + "-" * 60)
