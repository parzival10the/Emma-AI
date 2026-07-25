import json
import os
from datetime import datetime, time
from pathlib import Path
from threading import Thread
import time as time_module


class Scheduler:
    """Manages scheduling and reminders for Emma"""
    
    def __init__(self):
        self.schedules_file = "data/schedules.json"
        self.config_file = "data/emma_config.json"
        self.ensure_data_directory()
        self.load_schedules()
        self.running = False

    def ensure_data_directory(self):
        """Ensure data directory exists"""
        Path("data").mkdir(exist_ok=True)

    def load_schedules(self):
        """Load schedules from file"""
        if os.path.exists(self.schedules_file):
            with open(self.schedules_file, 'r') as f:
                self.schedules = json.load(f)
        else:
            self.schedules = {
                "daily_reminders": True,
                "reminder_times": {
                    "morning": "07:00",
                    "noon": "12:00",
                    "evening": "18:00"
                },
                "check_on_startup": True,
                "notifications_enabled": True
            }
            self.save_schedules()

    def save_schedules(self):
        """Save schedules to file"""
        with open(self.schedules_file, 'w') as f:
            json.dump(self.schedules, f, indent=2)

    def add_reminder(self, reminder_type, time_str, message):
        """Add a custom reminder"""
        reminder = {
            "type": reminder_type,
            "time": time_str,
            "message": message,
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
        
        if "custom_reminders" not in self.schedules:
            self.schedules["custom_reminders"] = []
        
        self.schedules["custom_reminders"].append(reminder)
        self.save_schedules()
        print(f"Emma: ✅ Reminder set for {time_str}!\n")

    def get_reminders_for_time(self, current_time):
        """Get all reminders that should trigger at current time"""
        reminders = []
        
        # Check daily reminders
        if self.schedules["daily_reminders"]:
            current_hour_min = current_time.strftime("%H:%M")
            for reminder_name, reminder_time in self.schedules["reminder_times"].items():
                if reminder_time == current_hour_min:
                    reminders.append({
                        "type": "daily",
                        "name": reminder_name,
                        "message": self.get_reminder_message(reminder_name)
                    })
        
        # Check custom reminders
        if "custom_reminders" in self.schedules:
            for reminder in self.schedules["custom_reminders"]:
                if reminder["enabled"] and reminder["time"] == current_time.strftime("%H:%M"):
                    reminders.append({
                        "type": "custom",
                        "message": reminder["message"]
                    })
        
        return reminders

    def get_reminder_message(self, reminder_type):
        """Get message for different reminder types"""
        messages = {
            "morning": "🌅 Good morning! Let's start the day right. Check your tasks!",
            "noon": "☀️ Mid-day check! Are you on track with your tasks?",
            "evening": "🌙 Evening check-in! How was your day? Let's review."
        }
        return messages.get(reminder_type, "Time to check your tasks!")

    def set_reminder_time(self, reminder_type, time_str):
        """Set or update a daily reminder time"""
        if reminder_type in self.schedules["reminder_times"]:
            self.schedules["reminder_times"][reminder_type] = time_str
            self.save_schedules()
            print(f"Emma: ✅ {reminder_type.capitalize()} reminder set to {time_str}!\n")
            return True
        return False

    def toggle_reminders(self, enabled=True):
        """Enable/disable all reminders"""
        self.schedules["daily_reminders"] = enabled
        self.save_schedules()
        status = "enabled" if enabled else "disabled"
        print(f"Emma: ✅ Daily reminders {status}!\n")

    def get_next_reminder(self):
        """Get next scheduled reminder"""
        current_time = datetime.now()
        reminder_times = self.schedules["reminder_times"]
        
        times = []
        for name, time_str in reminder_times.items():
            try:
                h, m = map(int, time_str.split(':'))
                times.append((h, m, name))
            except:
                pass
        
        times.sort()
        current_h = current_time.hour
        current_m = current_time.minute
        
        for h, m, name in times:
            if (h, m) > (current_h, current_m):
                return f"{h:02d}:{m:02d} - {name.capitalize()}"
        
        # Next day
        if times:
            h, m, name = times[0]
            return f"Tomorrow {h:02d}:{m:02d} - {name.capitalize()}"
        
        return "No reminders scheduled"

    def start_scheduler_daemon(self, task_manager):
        """Start background scheduler (run in separate thread)"""
        def run():
            self.running = True
            print("Emma: Scheduler daemon started! 🔔\n")
            
            last_check = None
            while self.running:
                try:
                    current_time = datetime.now()
                    current_minute = current_time.strftime("%H:%M")
                    
                    # Check every minute
                    if last_check != current_minute:
                        reminders = self.get_reminders_for_time(current_time)
                        
                        for reminder in reminders:
                            self.trigger_reminder(reminder, task_manager)
                        
                        last_check = current_minute
                    
                    time_module.sleep(10)  # Check every 10 seconds
                
                except Exception as e:
                    print(f"Emma: Scheduler error: {str(e)}\n")

        # Start in background thread
        scheduler_thread = Thread(target=run, daemon=True)
        scheduler_thread.start()

    def trigger_reminder(self, reminder, task_manager):
        """Trigger a reminder"""
        print("\n" + "=" * 50)
        print(f"🔔 {reminder['message']}")
        print("=" * 50)
        
        pending = task_manager.get_pending_tasks()
        if pending:
            print(f"\nYou have {len(pending)} pending tasks:")
            for task in pending[:5]:  # Show top 5
                icon = TaskManager.get_category_icon(task['category'])
                print(f"  {icon} {task['title']} ({task['category']})")
            if len(pending) > 5:
                print(f"  ... and {len(pending) - 5} more")
        else:
            print("\n✅ All tasks completed! Great job!")
        
        print("\n" + "=" * 50 + "\n")

    def stop_scheduler(self):
        """Stop the scheduler daemon"""
        self.running = False
        print("Emma: Scheduler stopped.\n")

    def list_schedules(self):
        """Display all schedules"""
        print("\n" + "=" * 50)
        print("🕐 Your Schedule")
        print("=" * 50)
        print("\nDaily Reminders:")
        if self.schedules["daily_reminders"]:
            for name, time_str in self.schedules["reminder_times"].items():
                print(f"  ✅ {name.capitalize()}: {time_str}")
        else:
            print("  ❌ Daily reminders disabled")
        
        if "custom_reminders" in self.schedules and self.schedules["custom_reminders"]:
            print("\nCustom Reminders:")
            for reminder in self.schedules["custom_reminders"]:
                status = "✅" if reminder["enabled"] else "❌"
                print(f"  {status} {reminder['time']}: {reminder['message']}")
        
        print("\n" + "=" * 50 + "\n")


# Import here to avoid circular import
class TaskManager:
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
