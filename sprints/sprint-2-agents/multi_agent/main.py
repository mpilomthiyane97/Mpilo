"""
Multi-Agent System Main Module
Orchestrates the multi-agent system with modular components
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from our modules
from memory_manager import ComprehensiveMemory
from tools import *
from agent_system import FourAgentSystem
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Initialize memory
memory = ComprehensiveMemory()

# Set memory instance for tools
set_memory_instance(memory)

async def main():
    """Main function for complete 4-agent learning system"""
    print("🚀 COMPLETE 4-AGENT LEARNING SYSTEM")
    print("="*70)
    print("Master advanced multi-agent orchestration:")
    print("Planner → Executor → Critic → Summariser")
    print("Learn: Full pipelines, synthesis, executive reporting, insights")
    print("="*70)
    
    # Check for API key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        print("❌ Please set OPENAI_API_KEY in your .env file")
        exit(1)
    
    # Create model client
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY,
    )
    
    # Create tools dictionary for agent system
    tools = {
        "create_task_tool": create_task_tool,
        "get_pending_tasks_tool": get_pending_tasks_tool,
        "complete_task_tool": complete_task_tool,
        "get_completed_tasks_tool": get_completed_tasks_tool,
        "review_task_tool": review_task_tool,
        "get_reviewed_tasks_tool": get_reviewed_tasks_tool,
        "create_summary_tool": create_summary_tool,
        "generate_insight_tool": generate_insight_tool,
        "get_project_overview_tool": get_project_overview_tool,
        "get_stats_tool": get_stats_tool
    }
    
    # Initialize the agent system
    system = FourAgentSystem(model_client, memory, tools)
    
    sample_goals = [
        "develop a comprehensive marketing strategy",
        "create a technical documentation system",
        "design a customer onboarding process",
        "build a project management framework"
    ]
    
    while True:
        print(f"\n🎛️ ADVANCED MULTI-AGENT WORKFLOWS")
        print("1. Complete Pipeline (Planner → Executor → Critic → Summariser)")
        print("2. Collaborative Workflow (All 4 agents together)")
        print("3. Iterative Improvement (Multi-cycle refinement)")
        print("4. Try sample enterprise goal")
        print("5. Enterprise Dashboard (System overview)")
        print("6. Project History Analysis")
        print("7. Clear memory (reset)")
        print("8. Exit")
        
        choice = input(f"\nSelect workflow (1-8): ").strip()
        
        if choice == "1":
            goal = input("Enter your goal: ").strip()
            if goal:
                await system.run_complete_pipeline(goal)
        
        elif choice == "2":
            goal = input("Enter your goal: ").strip()
            if goal:
                await system.run_collaborative_workflow(goal)
        
        elif choice == "3":
            goal = input("Enter your goal: ").strip()
            if goal:
                await system.run_iterative_improvement(goal)
        
        elif choice == "4":
            print("\nEnterprise Sample Goals:")
            for i, goal in enumerate(sample_goals, 1):
                print(f"{i}. {goal}")
            
            try:
                sample_choice = int(input("Choose sample (1-4): ")) - 1
                if 0 <= sample_choice < len(sample_goals):
                    workflow = input("Complete Pipeline (1), Collaborative (2), or Iterative (3)? ").strip()
                    if workflow == "1":
                        await system.run_complete_pipeline(sample_goals[sample_choice])
                    elif workflow == "2":
                        await system.run_collaborative_workflow(sample_goals[sample_choice])
                    elif workflow == "3":
                        await system.run_iterative_improvement(sample_goals[sample_choice])
            except ValueError:
                print("Invalid choice")
        
        elif choice == "5":
            system.show_enterprise_dashboard()
        
        elif choice == "6":
            # Show project history
            projects = memory.data["projects"]
            if projects:
                print(f"\n📚 PROJECT HISTORY")
                print("-" * 50)
                for project in projects:
                    status_emoji = "✅" if project["status"] == "completed" else "🔄"
                    print(f"{status_emoji} {project['goal']}")
                    print(f"   📅 {project['start_time'][:19]} | {project['workflow_type']}")
                    # if 'metrics' in project:
                    #     metrics = project['metrics']
                    #     print(f"   📊 {metrics.get('tasks_completed', 0)} tasks, {metrics.get('average_score', 0):.1f}/100 quality")
                    # print()
            else:
                print("No project history found.")
        
        elif choice == "7":
            memory.data = {
                "projects": [],
                "tasks": [],
                "conversations": [],
                "reviews": [],
                "debates": [],
                "summaries": [],
                "agent_stats": {
                    "Planner": {"tasks_created": 0, "projects_planned": 0},
                    "Executor": {"tasks_completed": 0, "execution_time": 0},
                    "Critic": {"reviews_completed": 0, "average_score": 0, "revisions_requested": 0},
                    "Summariser": {"summaries_created": 0, "insights_generated": 0}
                },
                "system_insights": []
            }
            memory.save()
            print("✅ Enterprise memory cleared!")
        
        elif choice == "8":
            print("🎊 Congratulations! You've mastered advanced multi-agent systems!")
            break
        
        else:
            print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())