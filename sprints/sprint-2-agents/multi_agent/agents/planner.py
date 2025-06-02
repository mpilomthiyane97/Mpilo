"""
Planner Agent for Multi-Agent System
Specializes in project planning and task breakdown
"""

from autogen_agentchat.agents import AssistantAgent

class PlannerAgent:
    """Planner agent that creates strategic plans and breaks down tasks"""
    
    def __init__(self, model_client, tools):
        """Initialize the Planner agent with model client and tools"""
        self.agent = AssistantAgent(
            name="Planner",
            model_client=model_client,
            system_message="""You are a strategic Planner agent. Your specialization is project planning and task breakdown.

Your tools:
- create_task_tool: Create specific, actionable tasks
- get_stats_tool: Check comprehensive system statistics

When given a goal:
1. Break it into 3-5 specific, executable tasks using create_task_tool
2. Create ONLY ONE SET of tasks - DO NOT create duplicate or similar tasks
3. Focus on content creation tasks, NOT distribution/sending
4. Create logical task sequences: draft → review → finalize → document
5. After creating all tasks, end with "Planning complete!"

IMPORTANT: Create each task EXACTLY ONCE. Check your work to ensure you haven't created duplicate tasks.

Be strategic and comprehensive in your planning.""",
            tools=tools
        )
    
    def get_agent(self):
        """Return the agent instance"""
        return self.agent
