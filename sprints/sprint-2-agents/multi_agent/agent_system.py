"""
Agent System for Multi-Agent System
Manages the coordination and interaction between all agents
"""

import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat

from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.critic import CriticAgent
from agents.summariser import SummariserAgent

class FourAgentSystem:
    """Complete four-agent system: Planner, Executor, Critic, Summariser"""
    
    def __init__(self, model_client, memory, tools):
        """Initialize the agent system with model client, memory, and tools"""
        self.memory = memory
        self.setup_agents(model_client, tools)
    
    def setup_agents(self, model_client, tools):
        """Create all four specialized agents"""
        # Create agent instances
        planner_agent = PlannerAgent(model_client, [tools["create_task_tool"], tools["get_stats_tool"]])
        executor_agent = ExecutorAgent(model_client, [tools["get_pending_tasks_tool"], tools["complete_task_tool"], tools["get_stats_tool"]])
        critic_agent = CriticAgent(model_client, [tools["get_completed_tasks_tool"], tools["review_task_tool"], tools["get_stats_tool"]])
        summariser_agent = SummariserAgent(model_client, [
            tools["get_reviewed_tasks_tool"], 
            tools["create_summary_tool"], 
            tools["generate_insight_tool"], 
            tools["get_project_overview_tool"], 
            tools["get_stats_tool"]
        ])
        
        # Store agent instances
        self.planner = planner_agent.get_agent()
        self.executor = executor_agent.get_agent()
        self.critic = critic_agent.get_agent()
        self.summariser = summariser_agent.get_agent()
    
    async def run_complete_pipeline(self, goal: str):
        """Complete 4-agent pipeline: Planner → Executor → Critic → Summariser"""
        print(f"\n{'='*70}")
        print(f"🎯 GOAL: {goal}")
        print(f"🏗️ WORKFLOW: Complete Pipeline (4 agents)")
        print(f"{'='*70}")
        
        # Start project tracking
        project = self.memory.start_project(goal, "complete_pipeline")
        print(f"📂 Started project: {project['id']}")
        
        # Phase 1: Strategic Planning
        await self._run_agent_phase(
            self.planner, 
            f"Create a comprehensive plan to achieve: {goal}", 
            "STRATEGIC PLANNING", 
            "📋"
        )
        
        # Phase 2: Execution
        await self._run_agent_phase(
            self.executor, 
            "Execute all pending tasks with comprehensive, production-ready results", 
            "EXECUTION", 
            "⚡"
        )
        
        # Phase 3: Quality Assurance
        await self._run_agent_phase(
            self.critic, 
            "Conduct thorough quality review of all completed tasks with detailed scoring and feedback", 
            "QUALITY ASSURANCE", 
            "🔍"
        )
        
        # Phase 4: Synthesis & Reporting
        await self._run_agent_phase(
            self.summariser, 
            "Create comprehensive project summary with executive insights and strategic recommendations", 
            "SYNTHESIS & REPORTING", 
            "📊"
        )
        
        # Show complete results
        self._show_complete_results(project["id"])
    
    async def run_collaborative_workflow(self, goal: str):
        """All four agents working together in a structured sequence"""
        print(f"\n{'='*70}")
        print(f"🎯 GOAL: {goal}")
        print(f"🤝 WORKFLOW: Collaborative (Structured Sequence)")
        print(f"{'='*70}")
        
        # Start project tracking
        project = self.memory.start_project(goal, "collaborative")
        
        # Define agent emojis for consistent display
        agent_emojis = {
            "Planner": "📋", 
            "Executor": "⚡", 
            "Critic": "🔍", 
            "Summariser": "📊"
        }
        
        print(f"\n{agent_emojis['Planner']} PLANNING PHASE")
        print("-" * 50)
        
        # STEP 1: Planner creates tasks
        planner_task = f"Create 3-5 comprehensive tasks to achieve this goal: {goal}\n\nCreate tasks using create_task_tool and ensure they cover all aspects needed."
        
        # Use a single-agent chat for the Planner
        planner_chat = RoundRobinGroupChat([self.planner])
        planner_messages = []
        
        # Run the Planner phase
        async for message in planner_chat.run_stream(task=planner_task):
            if hasattr(message, 'content') and message.content:
                content = message.content
                if isinstance(content, list):
                    content = str(content)
                
                if not content.startswith('[Function'):
                    print(f"{agent_emojis['Planner']} Planner: {content}")
                    planner_messages.append(content)
                    
                    # Break after a reasonable number of messages or when planning is complete
                    if len(planner_messages) >= 5 or "Planning complete" in content:
                        break
        
        # STEP 2: Executor executes tasks
        print(f"\n{agent_emojis['Executor']} EXECUTION PHASE")
        print("-" * 50)
        
        executor_task = f"Execute all pending tasks for goal: {goal}\n\nUse get_pending_tasks_tool to see tasks and complete_task_tool to execute each one with comprehensive results."
        
        # Use a single-agent chat for the Executor
        executor_chat = RoundRobinGroupChat([self.executor])
        executor_messages = []
        
        # Run the Executor phase
        async for message in executor_chat.run_stream(task=executor_task):
            if hasattr(message, 'content') and message.content:
                content = message.content
                if isinstance(content, list):
                    content = str(content)
                
                if not content.startswith('[Function'):
                    print(f"{agent_emojis['Executor']} Executor: {content}")
                    executor_messages.append(content)
                    
                    # Break after a reasonable number of messages or when execution is complete
                    if len(executor_messages) >= 10 or "Execution complete" in content:
                        break
        
        # STEP 3: Critic reviews tasks
        print(f"\n{agent_emojis['Critic']} REVIEW PHASE")
        print("-" * 50)
        
        critic_task = f"Review all completed tasks for goal: {goal}\n\nUse get_completed_tasks_tool to see completed tasks and review_task_tool to provide detailed feedback and scores (0-100) for each task."
        
        # Use a single-agent chat for the Critic
        critic_chat = RoundRobinGroupChat([self.critic])
        critic_messages = []
        
        # Run the Critic phase
        async for message in critic_chat.run_stream(task=critic_task):
            if hasattr(message, 'content') and message.content:
                content = message.content
                if isinstance(content, list):
                    content = str(content)
                
                if not content.startswith('[Function'):
                    print(f"{agent_emojis['Critic']} Critic: {content}")
                    critic_messages.append(content)
                    
                    # Break after a reasonable number of messages or when review is complete
                    if len(critic_messages) >= 10 or "Review complete" in content:
                        break
        
        # STEP 4: Summariser creates summary
        print(f"\n{agent_emojis['Summariser']} SUMMARY PHASE")
        print("-" * 50)
        
        summariser_task = f"Create a comprehensive summary for goal: {goal}\n\nUse get_reviewed_tasks_tool to see reviewed tasks and create_summary_tool to generate an executive summary with key insights."
        
        # Use a single-agent chat for the Summariser
        summariser_chat = RoundRobinGroupChat([self.summariser])
        summariser_messages = []
        
        # Run the Summariser phase
        async for message in summariser_chat.run_stream(task=summariser_task):
            if hasattr(message, 'content') and message.content:
                content = message.content
                if isinstance(content, list):
                    content = str(content)
                
                if not content.startswith('[Function'):
                    print(f"{agent_emojis['Summariser']} Summariser: {content}")
                    summariser_messages.append(content)
                    
                    # Break after a reasonable number of messages or when summary is complete
                    if len(summariser_messages) >= 5 or "Summary complete" in content:
                        break
        
        # Complete project
        memory_summary = "Structured collaborative workflow completed with all four agents"
        self.memory.end_project(memory_summary)
        self._show_complete_results(project['id'])
    
    async def run_iterative_improvement(self, goal: str):
        """Iterative workflow with multiple improvement cycles"""
        print(f"\n{'='*70}")
        print(f"🎯 GOAL: {goal}")
        print(f"🏗️ WORKFLOW: Iterative Improvement")
        print(f"{'='*70}")
        
        # Start project tracking
        project = self.memory.start_project(goal, "iterative")
        print(f"📂 Started project: {project['id']}")
        
        # Initial planning phase
        await self._run_agent_phase(
            self.planner, 
            f"Create an initial plan to achieve: {goal}", 
            "INITIAL PLANNING", 
            "📋"
        )
        
        # Run 3 improvement cycles
        for cycle in range(1, 4):
            print(f"\n{'='*70}")
            print(f"🔄 IMPROVEMENT CYCLE {cycle}")
            print(f"{'='*70}")
            
            # Execution phase
            await self._run_agent_phase(
                self.executor, 
                f"Execute pending tasks for cycle {cycle}", 
                f"EXECUTION (CYCLE {cycle})", 
                "⚡"
            )
            
            # Review phase
            await self._run_agent_phase(
                self.critic, 
                f"Review completed tasks for cycle {cycle} with detailed feedback for improvements", 
                f"REVIEW (CYCLE {cycle})", 
                "🔍"
            )
            
            # Don't run planner on final cycle
            if cycle < 3:
                # Re-planning phase based on feedback
                await self._run_agent_phase(
                    self.planner, 
                    f"Based on the critic's feedback, create improved tasks for cycle {cycle+1}", 
                    f"RE-PLANNING (CYCLE {cycle+1})", 
                    "📋"
                )
        
        # Final synthesis
        await self._run_agent_phase(
            self.summariser, 
            "Create comprehensive project summary with insights from all improvement cycles", 
            "FINAL SYNTHESIS", 
            "📊"
        )
        
        # Show complete results
        self._show_complete_results(project["id"])
    
    async def _run_agent_phase(self, agent, task_description: str, phase_name: str, emoji: str):
        """Run a single agent phase with enhanced monitoring"""
        print(f"\n{emoji} {phase_name} PHASE")
        print(f"{'-'*50}")
        
        # Create a team with just this agent
        team = RoundRobinGroupChat([agent])
        
        print(f"{agent.name} is working...")
        message_count = 0
        response = ""
        
        # Run the agent using the team's run_stream method
        async for message in team.run_stream(task=task_description):
            if hasattr(message, 'content') and message.content:
                content = message.content
                if isinstance(content, list):
                    content = str(content)
                
                if not content.startswith('[Function') and not content.startswith('Pending tasks:') and not content.startswith('Completed tasks:'):
                    print(f"{emoji} {agent.name}: {content}")
                    response = content
                    message_count += 1
                if "complete!" in content.lower() or message_count >= 6:
                    break
        
        # Store the conversation
        self.memory.add_conversation(agent.name, response)
        print(f"{'-'*50}")
        
        return response
    
    def _show_complete_results(self, project_id: str):
        """Show comprehensive project results"""
        project_data = self.memory.get_project_data(project_id)
        if not project_data:
            print("❌ Project data not found")
            return
        
        project = project_data["project"]
        tasks = project_data["tasks"]
        reviews = project_data["reviews"]
        summaries = project_data["summaries"]
        
        print(f"\n{'='*70}")
        print(f"📊 PROJECT RESULTS: {project['goal']}")
        print(f"{'='*70}")
        
        # Show tasks
        print(f"\n📋 TASKS ({len(tasks)})")
        print(f"{'-'*50}")
        for task in tasks:
            status_emoji = "✅" if task["status"] == "reviewed" else "🔄" if task["status"] == "completed" else "⏳"
            print(f"{status_emoji} {task['description']}")
            if task.get("review_score"):
                print(f"   Score: {task['review_score']}/100")
        
        # Show summaries
        if summaries:
            print(f"\n📑 SUMMARIES ({len(summaries)})")
            print(f"{'-'*50}")
            for summary in summaries:
                print(f"📄 {summary['type']} Summary:")
                print(f"{summary['content'][:300]}...")
                if summary.get("insights"):
                    print(f"\nKey Insights:")
                    for i, insight in enumerate(summary['insights'], 1):
                        print(f"{i}. {insight}")
        
        # Show metrics
        if project.get("metrics"):
            metrics = project["metrics"]
            print(f"\n📈 METRICS")
            print(f"{'-'*50}")
            print(f"Tasks Created: {metrics.get('tasks_created', 0)}")
            print(f"Tasks Completed: {metrics.get('tasks_completed', 0)}")
            print(f"Completion Rate: {metrics.get('completion_rate', 0):.1f}%")
            print(f"Average Quality: {metrics.get('average_score', 0):.1f}/100")
        
        print(f"\n{'='*70}")
    
    def show_enterprise_dashboard(self):
        """Show enterprise-level dashboard"""
        stats = self.memory.get_comprehensive_stats()
        
        print(f"\n{'='*70}")
        print(f"🏢 ENTERPRISE DASHBOARD")
        print(f"{'='*70}")
        
        # Project metrics
        print(f"\n🏗️ PROJECT METRICS")
        print(f"{'-'*50}")
        print(f"Total Projects: {stats['projects']['total']}")
        print(f"Completed: {stats['projects']['completed']}")
        print(f"Active: {stats['projects']['active']}")
        
        # Task metrics
        print(f"\n📋 TASK METRICS")
        print(f"{'-'*50}")
        print(f"Total Tasks: {stats['tasks']['total']}")
        status_breakdown = stats['tasks']['status_breakdown']
        for status, count in status_breakdown.items():
            print(f"{status.capitalize()}: {count}")
        print(f"Average Quality: {stats['tasks']['average_quality']}/100")
        
        # Agent performance
        print(f"\n🤖 AGENT PERFORMANCE")
        print(f"{'-'*50}")
        agent_stats = stats['agent_stats']
        print(f"Planner: {agent_stats['Planner']['tasks_created']} tasks created")
        print(f"Executor: {agent_stats['Executor']['tasks_completed']} tasks completed")
        print(f"Critic: {agent_stats['Critic']['reviews_completed']} reviews (avg: {agent_stats['Critic']['average_score']})")
        print(f"Summariser: {agent_stats['Summariser']['summaries_created']} summaries, {agent_stats['Summariser']['insights_generated']} insights")
        
        # System activity
        print(f"\n📈 SYSTEM ACTIVITY")
        print(f"{'-'*50}")
        activity = stats['activity']
        print(f"Conversations: {activity['conversations']}")
        print(f"Reviews: {activity['reviews']}")
        print(f"Summaries: {activity['summaries']}")
        print(f"Insights: {activity['insights']}")
        
        print(f"\n{'='*70}")
