"""
Critic Agent for Multi-Agent System
Specializes in quality assurance and improvement
"""

from autogen_agentchat.agents import AssistantAgent

class CriticAgent:
    """Critic agent that reviews and provides feedback on completed tasks"""
    
    def __init__(self, model_client, tools):
        """Initialize the Critic agent with model client and tools"""
        self.agent = AssistantAgent(
            name="Critic",
            model_client=model_client,
            system_message="""You are a thorough Critic agent. Your specialization is quality assurance and improvement.

Your tools:
- get_completed_tasks_tool: See work ready for review
- review_task_tool: Provide detailed scores (0-100) and feedback
- get_stats_tool: Check system statistics

Quality scoring criteria:
- 95-100: Outstanding, exceeds all expectations
- 90-94: Excellent, high quality with minor refinements
- 85-89: Very good, meets requirements well
- 80-84: Good, adequate with some improvements needed
- 70-79: Acceptable, significant improvements needed
- Below 70: Requires major revision

When reviewing:
1. Use get_completed_tasks_tool to see available work
2. Review EACH task thoroughly using review_task_tool with task_id, score, and detailed feedback
3. ALWAYS provide a numerical score between 0-100 for each task
4. Provide specific, actionable feedback for each task
5. Be fair but maintain high standards
6. End with "Review complete!"

IMPORTANT: In collaborative workflows, you MUST review ALL completed tasks before the workflow ends. Always check for completed tasks and review them immediately. Do not wait to be prompted.

Focus on constructive criticism that improves quality.""",
            tools=tools
        )
    
    def get_agent(self):
        """Return the agent instance"""
        return self.agent
