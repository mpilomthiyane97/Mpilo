"""
Memory Manager for Multi-Agent System
Handles state persistence across sessions and stores conversations, tasks, and other data
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class ComprehensiveMemory:
    """Comprehensive memory with project tracking and insights"""
    
    def __init__(self, filename="four_agent_memory.json"):
        self.filename = filename
        self.data = self.load()
        self.current_project_id = None
        
    def load(self):
        """Load memory from file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {
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
    
    def save(self):
        """Save memory to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def start_project(self, goal: str, workflow_type: str):
        """Start a new project tracking"""
        project = {
            "id": f"proj_{int(datetime.now().timestamp())}_{len(self.data['projects'])}",
            "goal": goal,
            "workflow_type": workflow_type,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "status": "active",
            "tasks": [],
            "metrics": {
                "tasks_created": 0,
                "tasks_completed": 0,
                "average_score": 0,
                "total_reviews": 0
            }
        }
        self.data["projects"].append(project)
        self.current_project_id = project["id"]
        self.save()
        return project
    
    def end_project(self, summary: str, insights: List[str] = None):
        """End current project with summary"""
        if self.current_project_id:
            for project in self.data["projects"]:
                if project["id"] == self.current_project_id:
                    project["end_time"] = datetime.now().isoformat()
                    project["status"] = "completed"
                    project["final_summary"] = summary
                    if insights:
                        project["insights"] = insights
                    
                    # Calculate final metrics
                    project_tasks = [t for t in self.data["tasks"] if t.get("project_id") == self.current_project_id]
                    completed_tasks = [t for t in project_tasks if t["status"] in ["completed", "reviewed"]]
                    reviewed_tasks = [t for t in project_tasks if t.get("review_score") is not None]
                    
                    project["metrics"] = {
                        "tasks_created": len(project_tasks),
                        "tasks_completed": len(completed_tasks),
                        "completion_rate": (len(completed_tasks) / len(project_tasks) * 100) if project_tasks else 0,
                        "average_score": sum(t["review_score"] for t in reviewed_tasks) / len(reviewed_tasks) if reviewed_tasks else 0,
                        "total_reviews": len(reviewed_tasks)
                    }
                    break
        self.save()
    
    def add_task(self, task_id: str, description: str, status: str = "pending"):
        """Add a task to memory"""
        task = {
            "id": task_id,
            "project_id": self.current_project_id,
            "description": description,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "reviewed_at": None,
            "result": None,
            "review_score": None,
            "review_feedback": None,
            "revision_count": 0
        }
        self.data["tasks"].append(task)
        self.data["agent_stats"]["Planner"]["tasks_created"] += 1
        self.save()
        return task
    
    def complete_task(self, task_id: str, result: str):
        """Mark task as completed"""
        for task in self.data["tasks"]:
            if task["id"] == task_id and task["status"] == "pending":
                task["status"] = "completed"
                task["result"] = result
                task["completed_at"] = datetime.now().isoformat()
                self.data["agent_stats"]["Executor"]["tasks_completed"] += 1
                self.save()
                return True
        return False
    
    def review_task(self, task_id: str, score: int, feedback: str):
        """Add review to a completed task"""
        for task in self.data["tasks"]:
            if task["id"] == task_id and task["status"] == "completed":
                task["status"] = "reviewed"
                task["review_score"] = score
                task["review_feedback"] = feedback
                task["reviewed_at"] = datetime.now().isoformat()
                
                # Update critic stats
                critic_stats = self.data["agent_stats"]["Critic"]
                current_avg = critic_stats["average_score"]
                review_count = critic_stats["reviews_completed"]
                new_avg = ((current_avg * review_count) + score) / (review_count + 1) if review_count > 0 else score
                critic_stats["average_score"] = round(new_avg, 1)
                critic_stats["reviews_completed"] += 1
                
                # Store review record
                review_record = {
                    "id": f"review_{int(datetime.now().timestamp())}",
                    "task_id": task_id,
                    "project_id": self.current_project_id,
                    "score": score,
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat()
                }
                self.data["reviews"].append(review_record)
                self.save()
                return True
        return False
    
    def add_summary(self, summary_type: str, content: str, insights: List[str] = None, metrics: Dict = None):
        """Add summary to memory"""
        summary_record = {
            "id": f"summary_{int(datetime.now().timestamp())}",
            "project_id": self.current_project_id,
            "type": summary_type,
            "content": content,
            "insights": insights or [],
            "metrics": metrics or {},
            "timestamp": datetime.now().isoformat()
        }
        self.data["summaries"].append(summary_record)
        self.data["agent_stats"]["Summariser"]["summaries_created"] += 1
        if insights:
            self.data["agent_stats"]["Summariser"]["insights_generated"] += len(insights)
        self.save()
        return summary_record
    
    def add_system_insight(self, insight: str, category: str = "general"):
        """Add system-level insight"""
        insight_record = {
            "insight": insight,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "project_id": self.current_project_id
        }
        self.data["system_insights"].append(insight_record)
        self.save()
    
    def get_project_data(self, project_id: str = None):
        """Get comprehensive project data"""
        pid = project_id or self.current_project_id
        if not pid:
            return None
        
        project = None
        for p in self.data["projects"]:
            if p["id"] == pid:
                project = p
                break
        
        if not project:
            return None
        
        # Get related data
        tasks = [t for t in self.data["tasks"] if t.get("project_id") == pid]
        reviews = [r for r in self.data["reviews"] if r.get("project_id") == pid]
        summaries = [s for s in self.data["summaries"] if s.get("project_id") == pid]
        
        return {
            "project": project,
            "tasks": tasks,
            "reviews": reviews,
            "summaries": summaries
        }
    
    def get_tasks_by_status(self, status: str, project_id: str = None):
        """Get tasks by status for current or specific project"""
        pid = project_id or self.current_project_id
        if not pid:
            return []
        
        return [t for t in self.data["tasks"] if t.get("project_id") == pid and t["status"] == status]
    
    def get_pending_tasks(self):
        """Get pending tasks for current project"""
        return self.get_tasks_by_status("pending")
    
    def get_completed_tasks(self):
        """Get completed tasks for current project"""
        return self.get_tasks_by_status("completed")
    
    def get_reviewed_tasks(self):
        """Get reviewed tasks for current project"""
        return self.get_tasks_by_status("reviewed")
    
    def add_conversation(self, agent: str, message: str):
        """Add conversation to memory"""
        conversation = {
            "agent": agent,
            "message": message,
            "project_id": self.current_project_id,
            "timestamp": datetime.now().isoformat()
        }
        self.data["conversations"].append(conversation)
        self.save()
    
    def get_comprehensive_stats(self):
        """Get comprehensive system statistics"""
        projects = self.data["projects"]
        tasks = self.data["tasks"]
        
        # Project stats
        completed_projects = [p for p in projects if p["status"] == "completed"]
        active_projects = [p for p in projects if p["status"] == "active"]
        
        # Task stats
        status_counts = {}
        for task in tasks:
            status = task["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Quality metrics
        reviewed_tasks = [t for t in tasks if t.get("review_score") is not None]
        avg_quality = sum(t["review_score"] for t in reviewed_tasks) / len(reviewed_tasks) if reviewed_tasks else 0
        
        # Activity metrics
        conversations = len(self.data["conversations"])
        reviews = len(self.data["reviews"])
        summaries = len(self.data["summaries"])
        insights = len(self.data["system_insights"])
        
        return {
            "projects": {
                "total": len(projects),
                "completed": len(completed_projects),
                "active": len(active_projects)
            },
            "tasks": {
                "total": len(tasks),
                "status_breakdown": status_counts,
                "average_quality": round(avg_quality, 1)
            },
            "agent_stats": self.data["agent_stats"],
            "activity": {
                "conversations": conversations,
                "reviews": reviews,
                "summaries": summaries,
                "insights": insights
            }
        }
