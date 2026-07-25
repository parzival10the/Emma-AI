import json
import os
from datetime import datetime
from pathlib import Path


class TaskManager:
    """Manages all tasks for Emma"""
    
    def __init__(self):
        self.data_file = "data/tasks.json"
        self.categories = ["Studies", "Messages", "Gym", "Food", "Other"]
        self.ensure_data_directory()
        self.load_tasks()

    def ensure_data_directory(self):
        """Ensure data directory exists"""
        Path("data").mkdir(exist_ok=True)

    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title, category="Other", deadline=None, priority="medium"):
        """Add a new task"""
        if category not in self.categories:
            category = "Other"
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "deadline": deadline,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        return task

    def complete_task(self, task_id):
        """Mark task as complete"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Emma: ✅ Great job! Task '{task['title']}' completed!\n")
                return True
        
        print(f"Emma: I couldn't find task with ID {task_id}.\n")
        return False

    def list_tasks(self, filter_by_category=None, show_completed=False):
        """List all tasks with optional filters"""
        print("\n" + "=" * 60)
        print("📝 Your Tasks")
        print("=" * 60)
        
        if not self.tasks:
            print("No tasks yet. Start by adding one!\n")
            return
        
        tasks_to_show = [
            t for t in self.tasks
            if (not filter_by_category or t['category'] == filter_by_category)
            and (show_completed or not t['completed'])
        ]
        
        if not tasks_to_show:
            print("No tasks to show.\n")
            return
        
        # Group by category
        by_category = {}
        for task in tasks_to_show:
            cat = task['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(task)
        
        for category in self.categories:
            if category in by_category:
                print(f"\n{self.get_category_icon(category)} {category}:")
                print("-" * 60)
                for task in by_category[category]:
                    self.print_task(task)
        
        print("=" * 60 + "\n")

    def print_task(self, task):
        """Print a single task in a formatted way"""
        status_icon = "✅" if task['completed'] else "⏳"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "")
        
        print(f"{status_icon} [{task['id']}] {task['title']} {priority_icon}")
        
        if task['deadline']:
            print(f"    Due: {task['deadline']}")
        
        if task['completed']:
            print(f"    Completed at: {task['completed_at'][:10]}")

    def get_pending_tasks(self):
        """Get all incomplete tasks"""
        return [t for t in self.tasks if not t['completed']]

    def get_all_tasks(self):
        """Get all tasks"""
        return self.tasks

    def get_tasks_by_category(self, category):
        """Get tasks by category"""
        return [t for t in self.tasks if t['category'] == category and not t['completed']]

    def get_overdue_tasks(self):
        """Get tasks that are past their deadline"""
        overdue = []
        for task in self.tasks:
            if not task['completed'] and task['deadline']:
                try:
                    deadline = datetime.fromisoformat(task['deadline'].split('T')[0])
                    if deadline < datetime.now().date():
                        overdue.append(task)
                except:
                    pass
        return overdue

    def update_task(self, task_id, **kwargs):
        """Update task properties"""
        for task in self.tasks:
            if task["id"] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()
        print(f"Emma: Task deleted successfully.\n")

    @staticmethod
    def get_category_icon(category):
        """Get emoji icon for category"""
        icons = {
            "Studies": "📚",
            "Messages": "📱",
            "Gym": "💪",
            "Food": "🍔",
            "Other": "✨"
        }
        return icons.get(category, "✨")

    def get_stats(self):
        """Get task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        by_category = {}
        for cat in self.categories:
            count = sum(1 for t in self.tasks if t['category'] == cat and not t['completed'])
            if count > 0:
                by_category[cat] = count
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_category": by_category,
            "overdue": len(self.get_overdue_tasks())
        }
