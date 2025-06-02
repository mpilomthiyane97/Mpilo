"""
Tool functions for Multi-Agent System
Contains all the tools that agents can use to interact with the memory system
"""

import uuid
from typing import List

# This will be imported from main.py
memory = None

def set_memory_instance(memory_instance):
    """Set the memory instance for tools to use"""
    global memory
    memory = memory_instance

def create_task_tool(description: str) -> str:
    """Tool for Planner to create tasks"""
    import time
    import random
    task_id = f"task_{int(time.time())}_{random.randint(100, 999)}"
    task = memory.add_task(task_id, description)
    return f"✅ Created task: {task_id}\n{description}"

def get_pending_tasks_tool() -> str:
    """Tool to get all pending tasks"""
    tasks = memory.get_pending_tasks()
    if not tasks:
        return "No pending tasks found."
    
    result = "📋 Pending Tasks:\n"
    for i, task in enumerate(tasks, 1):
        result += f"{i}. ID: {task['id']}\n   {task['description']}\n"
    return result

def complete_task_tool(task_id: str, result: str) -> str:
    """Tool for Executor to complete tasks"""
    success = memory.complete_task(task_id, result)
    if success:
        return f"✅ Completed task: {task_id}"
    return f"❌ Failed to complete task: {task_id} (not found or not pending)"

def get_completed_tasks_tool() -> str:
    """Tool to get all completed tasks for review"""
    tasks = memory.get_completed_tasks()
    if not tasks:
        return "No completed tasks found for review."
    
    result = "📋 Completed Tasks Ready for Review:\n"
    for i, task in enumerate(tasks, 1):
        result += f"{i}. ID: {task['id']}\n   Description: {task['description']}\n"
        result += f"   Result: {task['result'][:100]}...\n" if len(task['result']) > 100 else f"   Result: {task['result']}\n"
    return result

def review_task_tool(task_id: str, score: int, feedback: str) -> str:
    """Tool for Critic to review completed tasks"""
    success = memory.review_task(task_id, score, feedback)
    if success:
        return f"✅ Reviewed task: {task_id}\nScore: {score}/100\nFeedback: {feedback}"
    return f"❌ Failed to review task: {task_id} (not found or not completed)"

def get_reviewed_tasks_tool() -> str:
    """Tool to get all reviewed tasks for summarization"""
    tasks = memory.get_reviewed_tasks()
    if not tasks:
        return "No reviewed tasks found for summarization."
    
    result = "📋 Reviewed Tasks Ready for Summarization:\n"
    for i, task in enumerate(tasks, 1):
        result += f"{i}. ID: {task['id']}\n   Description: {task['description']}\n"
        result += f"   Score: {task['review_score']}/100\n"
        result += f"   Feedback: {task['review_feedback']}\n"
    return result

def create_summary_tool(summary_type: str, content: str, insights: str = "") -> str:
    """Tool for Summariser to create project summaries"""
    # Parse insights string into list
    insight_list = []
    if insights:
        # Split by numbered list items or bullet points
        if any(f"{i}." in insights for i in range(1, 10)):
            # Numbered list
            parts = insights.split("\n")
            for part in parts:
                if any(part.strip().startswith(f"{i}.") for i in range(1, 10)):
                    cleaned = part.strip()
                    # Remove the number prefix
                    for i in range(1, 10):
                        if cleaned.startswith(f"{i}."):
                            cleaned = cleaned[len(f"{i}."):].strip()
                            break
                    insight_list.append(cleaned)
        elif "•" in insights or "-" in insights:
            # Bullet points
            parts = insights.split("\n")
            for part in parts:
                if part.strip().startswith("•") or part.strip().startswith("-"):
                    cleaned = part.strip()[1:].strip()  # Remove bullet and trim
                    insight_list.append(cleaned)
        else:
            # Just split by lines
            insight_list = [line.strip() for line in insights.split("\n") if line.strip()]
    
    # Create the summary
    summary = memory.add_summary(summary_type, content, insight_list)
    
    return f"✅ Created {summary_type} summary with {len(insight_list)} insights"

def generate_insight_tool(insight: str, category: str = "general") -> str:
    """Tool for Summariser to generate system insights"""
    memory.add_system_insight(insight, category)
    return f"✅ Added system insight: {insight} (category: {category})"

def get_project_overview_tool() -> str:
    """Tool to get current project overview"""
    project_data = memory.get_project_data()
    if not project_data:
        return "No active project found."
    
    project = project_data["project"]
    tasks = project_data["tasks"]
    reviews = project_data["reviews"]
    
    # Calculate metrics
    pending_tasks = [t for t in tasks if t["status"] == "pending"]
    completed_tasks = [t for t in tasks if t["status"] == "completed"]
    reviewed_tasks = [t for t in tasks if t["status"] == "reviewed"]
    
    # Calculate average score safely to avoid division by zero
    avg_score = sum(r['score'] for r in reviews) / len(reviews) if reviews else 0
    
    result = f"""📊 Project Overview: {project['goal']}
ID: {project['id']}
Status: {project['status']}
Workflow: {project['workflow_type']}
Started: {project['start_time'][:19]}

📈 Progress:
Tasks: {len(tasks)} total
- Pending: {len(pending_tasks)}
- Completed: {len(completed_tasks)}
- Reviewed: {len(reviewed_tasks)}

Reviews: {len(reviews)} completed
Average Score: {avg_score:.1f}/100
"""
    return result

def get_stats_tool() -> str:
    """Tool to get comprehensive system statistics"""
    stats = memory.get_comprehensive_stats()
    
    result = f"""📊 Comprehensive System Statistics:

🏗️ Projects:
- Total: {stats['projects']['total']}
- Completed: {stats['projects']['completed']}
- Active: {stats['projects']['active']}

📋 Tasks:
- Total: {stats['tasks']['total']}
- Status: {stats['tasks']['status_breakdown']}
- Average Quality: {stats['tasks']['average_quality']}/100

🤖 Agent Performance:
- Planner: {stats['agent_stats']['Planner']['tasks_created']} tasks created, {stats['agent_stats']['Planner']['projects_planned']} projects planned
- Executor: {stats['agent_stats']['Executor']['tasks_completed']} tasks completed
- Critic: {stats['agent_stats']['Critic']['reviews_completed']} reviews (avg: {stats['agent_stats']['Critic']['average_score']})
- Summariser: {stats['agent_stats']['Summariser']['summaries_created']} summaries, {stats['agent_stats']['Summariser']['insights_generated']} insights

📈 Activity:
- Conversations: {stats['activity']['conversations']}
- Reviews: {stats['activity']['reviews']}
- Summaries: {stats['activity']['summaries']}
- Insights: {stats['activity']['insights']}"""
    
    return result
