import json
import os
from datetime import datetime
from pathlib import Path


class Memory:
    """Emma's memory system - stores preferences, patterns, and conversation history"""
    
    def __init__(self):
        self.memory_file = "memory/user_memory.json"
        self.conversation_file = "memory/conversations.jsonl"
        self.patterns_file = "memory/patterns.json"
        self.ensure_memory_directory()
        self.load_memory()

    def ensure_memory_directory(self):
        """Ensure memory directory exists"""
        Path("memory").mkdir(exist_ok=True)

    def load_memory(self):
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "preferences": {
                    "favorite_study_time": None,
                    "gym_frequency": None,
                    "preferred_notification_time": None,
                    "favorite_motivational_quotes": []
                },
                "habits": {
                    "typical_study_hours": 0,
                    "gym_sessions_per_week": 0,
                    "meal_times": [],
                    "message_response_time": None
                },
                "achievements": [],
                "streaks": {},
                "last_interaction": None,
                "total_interactions": 0
            }
            self.save_memory()

    def save_memory(self):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def record_conversation(self, user_input, emma_response):
        """Record conversation for learning"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "emma": emma_response
        }
        
        with open(self.conversation_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def update_preference(self, key, value):
        """Update a user preference"""
        if key in self.memory["preferences"]:
            self.memory["preferences"][key] = value
            self.save_memory()
            return True
        return False

    def update_habit(self, habit_name, value):
        """Update a habit entry"""
        if habit_name in self.memory["habits"]:
            self.memory["habits"][habit_name] = value
            self.save_memory()
            return True
        return False

    def add_achievement(self, achievement):
        """Record an achievement"""
        achievement_entry = {
            "title": achievement,
            "date": datetime.now().isoformat()
        }
        self.memory["achievements"].append(achievement_entry)
        self.save_memory()

    def get_achievements(self):
        """Get all achievements"""
        return self.memory["achievements"]

    def update_streak(self, task_category):
        """Update streak for a task category"""
        if task_category not in self.memory["streaks"]:
            self.memory["streaks"][task_category] = {
                "count": 1,
                "last_updated": datetime.now().isoformat()
            }
        else:
            last_update = datetime.fromisoformat(self.memory["streaks"][task_category]["last_updated"])
            today = datetime.now().date()
            last_update_date = last_update.date()
            
            if last_update_date == today:
                pass  # Already counted today
            elif (today - last_update_date).days == 1:
                self.memory["streaks"][task_category]["count"] += 1
            else:
                self.memory["streaks"][task_category]["count"] = 1
            
            self.memory["streaks"][task_category]["last_updated"] = datetime.now().isoformat()
        
        self.save_memory()

    def get_streak(self, task_category):
        """Get streak for a task category"""
        if task_category in self.memory["streaks"]:
            return self.memory["streaks"][task_category]["count"]
        return 0

    def get_conversation_history(self, limit=10):
        """Get recent conversation history"""
        if not os.path.exists(self.conversation_file):
            return []
        
        conversations = []
        with open(self.conversation_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                conversations.append(json.loads(line))
        
        return conversations

    def get_user_insights(self):
        """Generate insights about user patterns"""
        insights = {
            "total_interactions": self.memory["total_interactions"],
            "achievements_count": len(self.memory["achievements"]),
            "active_streaks": {k: v["count"] for k, v in self.memory["streaks"].items() if v["count"] > 0},
            "preferences": self.memory["preferences"],
            "habits": self.memory["habits"]
        }
        return insights

    def get_motivational_message(self):
        """Get a personalized motivational message based on memory"""
        quotes = [
            "You've got this! Keep pushing forward! 💪",
            "Progress, not perfection! You're doing great! 🌟",
            "Every task completed is a step forward! 🎯",
            "You're building great habits! Keep it up! 🚀",
            "Your future self will thank you! 📚",
            "Believe in yourself! You're capable of amazing things! ✨"
        ]
        
        streaks = self.get_user_insights()["active_streaks"]
        if streaks:
            highest_streak = max(streaks.values())
            if highest_streak >= 7:
                return f"Amazing! You have a {highest_streak}-day streak! Keep it going! 🔥"
            elif highest_streak >= 3:
                return f"Great work! {highest_streak}-day streak in progress! Don't break it! 💪"
        
        import random
        return random.choice(quotes)

    def analyze_productivity(self):
        """Analyze user productivity patterns"""
        history = self.get_conversation_history(limit=100)
        
        if not history:
            return "No data yet to analyze productivity."
        
        task_types = {}
        for entry in history:
            if "task" in entry["user"].lower():
                for category in ["Studies", "Gym", "Food", "Messages"]:
                    if category.lower() in entry["user"].lower():
                        task_types[category] = task_types.get(category, 0) + 1
        
        analysis = "📊 Productivity Analysis:\n"
        if task_types:
            analysis += "Most focused on: " + max(task_types, key=task_types.get) + "\n"
        
        return analysis

    def log_interaction(self):
        """Log an interaction"""
        self.memory["total_interactions"] += 1
        self.memory["last_interaction"] = datetime.now().isoformat()
        self.save_memory()

    def get_greeting_with_memory(self, creator_name):
        """Get a personalized greeting based on memory"""
        insights = self.get_user_insights()
        streaks = insights["active_streaks"]
        
        hour = datetime.now().hour
        base_greeting = f"Hello {creator_name}! "
        
        if hour < 12:
            greeting = f"🌅 Good morning {creator_name}! "
        elif hour < 18:
            greeting = f"☀️ Good afternoon {creator_name}! "
        else:
            greeting = f"🌙 Good evening {creator_name}! "
        
        if streaks:
            longest_streak = max(streaks.values())
            longest_category = [k for k, v in streaks.items() if v == longest_streak][0]
            greeting += f"\nYou're on a {longest_streak}-day {longest_category} streak! Keep it up! 🔥"
        
        return greeting
