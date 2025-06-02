"""
Executor Agent for Multi-Agent System
Specializes in high-quality task execution
"""

from autogen_agentchat.agents import AssistantAgent

class ExecutorAgent:
    """Executor agent that completes tasks with high quality"""
    
    def __init__(self, model_client, tools):
        """Initialize the Executor agent with model client and tools"""
        self.agent = AssistantAgent(
            name="Executor",
            model_client=model_client,
            system_message="""You are a skilled Executor agent. Your specialization is high-quality task execution.

Your tools:
- get_pending_tasks_tool: See current tasks
- complete_task_tool: Complete tasks with detailed results
- get_stats_tool: Check system statistics

When executing tasks:
1. Use get_pending_tasks_tool to see what needs to be done
2. For EACH pending task, use complete_task_tool with the EXACT task_id and COMPREHENSIVE results
3. Provide full content, not summaries or placeholders
4. Ensure deliverables are production-ready
5. ALWAYS check if there are more pending tasks after completing one
6. End with "Execution complete!" only when ALL tasks are completed

IMPORTANT: You MUST execute ALL pending tasks before finishing. Each task must be completed with detailed, high-quality results.

Focus on excellence and completeness in all deliverables.""",
            tools=tools
        )
    
    def get_agent(self):
        """Return the agent instance"""
        return self.agent
