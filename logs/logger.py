import json
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """Emma's logging system - tracks all activities and events"""
    
    def __init__(self):
        self.logs_file = "logs/activity.jsonl"
        self.stats_file = "logs/statistics.json"
        self.ensure_logs_directory()

    def ensure_logs_directory(self):
        """Ensure logs directory exists"""
        Path("logs").mkdir(exist_ok=True)

    def log_activity(self, activity_type, description, metadata=None):
        """Log an activity"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "description": description,
            "metadata": metadata or {}
        }
        
        with open(self.logs_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def log_task_created(self, task_id, title, category):
        """Log when a task is created"""
        self.log_activity("task_created", f"Created task: {title}", {
            "task_id": task_id,
            "category": category,
            "title": title
        })

    def log_task_completed(self, task_id, title, category):
        """Log when a task is completed"""
        self.log_activity("task_completed", f"Completed task: {title}", {
            "task_id": task_id,
            "category": category,
            "title": title
        })

    def log_reminder(self, reminder_type, message):
        """Log when a reminder is triggered"""
        self.log_activity("reminder_triggered", f"{reminder_type}: {message}", {
            "reminder_type": reminder_type
        })

    def log_check_in(self, pending_count, completed_count):
        """Log daily check-in"""
        self.log_activity("check_in", "Daily check-in performed", {
            "pending_tasks": pending_count,
            "completed_tasks": completed_count
        })

    def get_daily_summary(self):
        """Get summary of today's activities"""
        if not os.path.exists(self.logs_file):
            return {}
        
        today = datetime.now().date()
        activities = {}
        
        with open(self.logs_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_date = datetime.fromisoformat(entry["timestamp"]).date()
                
                if entry_date == today:
                    activity_type = entry["type"]
                    if activity_type not in activities:
                        activities[activity_type] = 0
                    activities[activity_type] += 1
        
        return activities

    def get_statistics(self):
        """Get overall statistics"""
        if not os.path.exists(self.logs_file):
            return {}
        
        stats = {
            "total_tasks_created": 0,
            "total_tasks_completed": 0,
            "total_check_ins": 0,
            "total_reminders": 0
        }
        
        with open(self.logs_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                
                if entry["type"] == "task_created":
                    stats["total_tasks_created"] += 1
                elif entry["type"] == "task_completed":
                    stats["total_tasks_completed"] += 1
                elif entry["type"] == "check_in":
                    stats["total_check_ins"] += 1
                elif entry["type"] == "reminder_triggered":
                    stats["total_reminders"] += 1
        
        self.save_statistics(stats)
        return stats

    def save_statistics(self, stats):
        """Save statistics to file"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

    def get_weekly_report(self):
        """Get weekly activity report"""
        from datetime import timedelta
        
        if not os.path.exists(self.logs_file):
            return {}
        
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        report = {}
        
        with open(self.logs_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_date = datetime.fromisoformat(entry["timestamp"]).date()
                
                if week_ago <= entry_date <= today:
                    date_str = entry_date.isoformat()
                    if date_str not in report:
                        report[date_str] = {}
                    
                    activity_type = entry["type"]
                    if activity_type not in report[date_str]:
                        report[date_str][activity_type] = 0
                    report[date_str][activity_type] += 1
        
        return report

    def print_daily_summary(self):
        """Print today's summary"""
        summary = self.get_daily_summary()
        
        print("\n" + "=" * 50)
        print("📅 Today's Summary")
        print("=" * 50)
        
        if not summary:
            print("No activities logged yet today.")
        else:
            for activity_type, count in summary.items():
                icon = "📝" if activity_type == "task_created" else \
                       "✅" if activity_type == "task_completed" else \
                       "🔔" if activity_type == "reminder_triggered" else \
                       "📋" if activity_type == "check_in" else "📌"
                
                print(f"{icon} {activity_type.replace('_', ' ').title()}: {count}")
        
        print("=" * 50 + "\n")

    def print_statistics(self):
        """Print overall statistics"""
        stats = self.get_statistics()
        
        print("\n" + "=" * 50)
        print("📊 Overall Statistics")
        print("=" * 50)
        
        if not any(stats.values()):
            print("No statistics recorded yet.")
        else:
            print(f"📝 Tasks Created: {stats.get('total_tasks_created', 0)}")
            print(f"✅ Tasks Completed: {stats.get('total_tasks_completed', 0)}")
            print(f"📋 Check-ins: {stats.get('total_check_ins', 0)}")
            print(f"🔔 Reminders: {stats.get('total_reminders', 0)}")
            
            completed = stats.get('total_tasks_completed', 0)
            created = stats.get('total_tasks_created', 0)
            if created > 0:
                completion_rate = (completed / created) * 100
                print(f"✨ Completion Rate: {completion_rate:.1f}%")
        
        print("=" * 50 + "\n")
