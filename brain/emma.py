from datetime import datetime
import json
import os


class Emma:
    """Emma - Your daily task manager AI assistant"""
    
    def __init__(self, name="Emma", creator="Parzival", version="2.0"):
        self.name = name
        self.version = version
        self.creator = creator
        self.start_time = datetime.now()
        self.config_file = "data/emma_config.json"
        self.last_check_in = None
        self.load_config()

    def load_config(self):
        """Load Emma's configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "creator": self.creator,
                "reminders": {
                    "morning": "07:00",
                    "noon": "12:00",
                    "evening": "18:00"
                },
                "personality": "helpful, caring, motivating",
                "categories": ["Studies", "Messages", "Gym", "Food", "Other"]
            }
            os.makedirs("data", exist_ok=True)
            self.save_config()

    def save_config(self):
        """Save Emma's configuration"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def boot(self):
        """Boot up Emma with status display"""
        print("=" * 50)
        print(f" {self.name} AI - Daily Task Manager")
        print("=" * 50)
        print(f"Version      : {self.version}")
        print(f"Creator      : {self.creator}")
        print("Status       : ONLINE 🟢")
        print(f"Boot Time    : {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        print(f"\n💬 Hello {self.creator}!")
        print("I'm Emma, your AI assistant for managing daily tasks.")
        print("I'll help you with:")
        print("  📚 Studies - Track assignments, deadlines")
        print("  📱 Messages - Reminders for important communications")
        print("  💪 Gym - Fitness goals and workouts")
        print("  🍔 Food - Meal tracking and nutrition")
        print("  ✨ And much more!\n")
        print("I'll check on you regularly and keep you motivated.")
        print("=" * 50 + "\n")

    def get_greeting(self):
        """Get a contextual greeting based on time"""
        hour = datetime.now().hour
        if hour < 12:
            return f"Good morning, {self.creator}! 🌅"
        elif hour < 18:
            return f"Good afternoon, {self.creator}! ☀️"
        else:
            return f"Good evening, {self.creator}! 🌙"

    def start_interactive_mode(self, task_manager, scheduler, memory, logger):
        """Start Emma's interactive conversation mode"""
        print(self.get_greeting())
        print("Type 'help' for available commands or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    response = "Thank you for using me! Take care and stay productive! 👋"
                    print(f"Emma: {response}\n")
                    memory.record_conversation(user_input, response)
                    logger.log_activity("shutdown", "Emma closed by user")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                
                elif user_input.lower() == 'check':
                    self.daily_check_in(task_manager, logger)
                
                elif user_input.lower().startswith('add task'):
                    parts = user_input.replace('add task', '', 1).strip().split('|')
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        category = parts[1].strip() if len(parts) > 1 else "Other"
                        deadline = parts[2].strip() if len(parts) > 2 else None
                        task = task_manager.add_task(title, category, deadline)
                        response = f"✅ Added '{title}' to your {category} tasks!"
                        print(f"Emma: {response}\n")
                        memory.record_conversation(user_input, response)
                        logger.log_task_created(task["id"], title, category)
                    else:
                        print("Emma: Use format: add task <title> | <category> | [deadline]\n")
                
                elif user_input.lower() == 'list tasks':
                    task_manager.list_tasks()
                
                elif user_input.lower().startswith('complete'):
                    parts = user_input.replace('complete', '', 1).strip()
                    if parts.isdigit():
                        task_id = int(parts)
                        tasks = task_manager.get_all_tasks()
                        task = next((t for t in tasks if t["id"] == task_id), None)
                        if task:
                            task_manager.complete_task(task_id)
                            memory.update_streak(task["category"])
                            logger.log_task_completed(task_id, task["title"], task["category"])
                            memory.record_conversation(user_input, f"✅ Task completed!")
                    else:
                        print("Emma: Please specify task ID (e.g., 'complete 1')\n")
                
                elif user_input.lower() == 'status':
                    self.show_status(task_manager)
                
                elif user_input.lower() == 'stats':
                    logger.print_statistics()
                    memory_insights = memory.get_user_insights()
                    print("🧠 Memory Insights:")
                    print(f"  Total Interactions: {memory_insights['total_interactions']}")
                    print(f"  Achievements: {memory_insights['achievements_count']}")
                    if memory_insights['active_streaks']:
                        print(f"  Active Streaks: {memory_insights['active_streaks']}\n")
                
                elif user_input.lower() == 'achievements':
                    self.show_achievements(memory)
                
                elif user_input.lower() == 'motivation':
                    message = memory.get_motivational_message()
                    print(f"Emma: {message}\n")
                    memory.record_conversation(user_input, message)
                
                elif user_input.lower() == 'summary':
                    logger.print_daily_summary()
                
                elif user_input.lower() == 'weekly':
                    weekly = logger.get_weekly_report()
                    print("\n" + "=" * 50)
                    print("📊 Weekly Activity Report")
                    print("=" * 50)
                    if weekly:
                        for date, activities in sorted(weekly.items()):
                            print(f"\n{date}:")
                            for activity, count in activities.items():
                                print(f"  - {activity.replace('_', ' ').title()}: {count}")
                    else:
                        print("No weekly data available yet.")
                    print("=" * 50 + "\n")
                
                elif user_input.lower() == 'register face':
                    self.handle_face_registration()
                
                elif user_input.lower() == 'recognize':
                    self.handle_face_recognition()
                
                elif user_input.lower() == 'faces':
                    self.show_registered_faces()
                
                elif user_input.lower() == 'check emails':
                    self.check_emails(task_manager)
                
                elif user_input.lower().startswith('search emails'):
                    keyword = user_input.replace('search emails', '', 1).strip()
                    self.search_emails(keyword)
                
                elif user_input.lower() == 'email summary':
                    self.show_email_summary()
                
                elif user_input.lower() == 'email stats':
                    self.show_email_stats()
                
                elif user_input.lower().startswith('emails from'):
                    sender = user_input.replace('emails from', '', 1).strip()
                    self.show_emails_from(sender)
                
                else:
                    response = self.respond_conversationally(user_input)
                    memory.record_conversation(user_input, response.replace("Emma: ", "").replace("\n", ""))
            
            except KeyboardInterrupt:
                print("\n\nEmma: Goodbye! Stay productive! 👋")
                break
            except Exception as e:
                print(f"Emma: I encountered an error: {str(e)}\n")

    def daily_check_in(self, task_manager, logger):
        """Perform daily check-in with user"""
        print("\n" + "=" * 50)
        print(f"{self.get_greeting()}")
        print("=" * 50)
        print("\n📋 Daily Check-In Time!")
        print("-" * 50)
        
        tasks = task_manager.get_pending_tasks()
        
        if not tasks:
            print("Emma: Great! You don't have any pending tasks. Take some rest! 🌟\n")
        else:
            print(f"Emma: You have {len(tasks)} pending tasks today:\n")
            for i, task in enumerate(tasks, 1):
                status_icon = "⏳" if not task['completed'] else "✅"
                print(f"{status_icon} [{task['id']}] {task['title']}")
                print(f"   Category: {task['category']}")
                if task.get('deadline'):
                    print(f"   Due: {task['deadline']}")
                print()
        
        completed = sum(1 for t in task_manager.get_all_tasks() if t['completed'])
        logger.log_check_in(len(tasks), completed)
        print("-" * 50 + "\n")

    def show_status(self, task_manager):
        """Show overall status"""
        tasks = task_manager.get_all_tasks()
        completed = sum(1 for t in tasks if t['completed'])
        total = len(tasks)
        
        print(f"\n📊 Status Report")
        print("-" * 40)
        print(f"Total Tasks: {total}")
        print(f"Completed: {completed}/{total}")
        if total > 0:
            print(f"Progress: {(completed/total)*100:.1f}%")
        print("-" * 40 + "\n")

    def show_help(self):
        """Show available commands"""
        print("\n" + "=" * 60)
        print("📖 Available Commands:")
        print("=" * 60)
        print("Task Management:")
        print("  add task <title> | <category> | [deadline]  - Add a new task")
        print("  list tasks                                  - Show all tasks")
        print("  complete <id>                              - Mark task as done")
        print("\nDaily Activities:")
        print("  check                                       - Daily check-in")
        print("  status                                      - Show progress")
        print("  summary                                     - Today's summary")
        print("  weekly                                      - Weekly report")
        print("\nEmail Management:")
        print("  check emails                                - Check unread emails")
        print("  email summary                               - Email summary")
        print("  search emails <keyword>                     - Search emails")
        print("  emails from <sender>                        - Emails from sender")
        print("  email stats                                 - Email statistics")
        print("\nAnalytics & Learning:")
        print("  stats                                       - View statistics")
        print("  achievements                                - View achievements")
        print("  motivation                                  - Get motivated!")
        print("\nFace Recognition:")
        print("  register face                              - Register your face")
        print("  recognize                                  - Recognize face")
        print("  faces                                       - Show registered faces")
        print("\nOther:")
        print("  help                                        - Show this help")
        print("  quit                                        - Exit Emma")
        print("=" * 60 + "\n")

    def show_achievements(self, memory):
        """Show achievements"""
        achievements = memory.get_achievements()
        
        print("\n" + "=" * 50)
        print("🏆 Your Achievements")
        print("=" * 50)
        
        if not achievements:
            print("No achievements yet. Keep working to earn some! 🚀")
        else:
            for i, achievement in enumerate(achievements, 1):
                date = achievement["date"].split("T")[0]
                print(f"{i}. {achievement['title']}")
                print(f"   Unlocked on: {date}")
        
        print("=" * 50 + "\n")

    def respond_conversationally(self, user_input):
        """Generate conversational responses"""
        keywords = {
            'motivation': "You've got this! Keep pushing forward! 💪",
            'tired': "Take a break, you deserve it! Rest is important too. 😌",
            'help': "I'm here to help! Tell me what you need.",
            'task': "Let me help you with that task!",
            'study': "Focus on your studies! You'll do great! 📚",
            'gym': "Amazing! Keep up your fitness goals! 💪",
            'food': "Eat well and stay healthy! 🍎",
            'message': "I'll help you stay on top of your messages! 📱",
        }
        
        response = "I'm here to help! Feel free to add tasks, check your progress, or chat with me. 😊"
        
        for keyword, reply in keywords.items():
            if keyword in user_input.lower():
                response = reply
                break
        
        print(f"Emma: {response}\n")
        return response

    def handle_face_registration(self):
        """Handle face registration"""
        try:
            from brain.facial_recognition import FacialRecognition
            facial_system = FacialRecognition()
            facial_system.register_face(self.creator)
        except ImportError:
            print("Emma: Face recognition not available. Install with:\n")
            print("pip install opencv-python face-recognition pillow numpy\n")
        except Exception as e:
            print(f"Emma: Error during registration: {str(e)}\n")

    def handle_face_recognition(self):
        """Handle face recognition"""
        try:
            from brain.facial_recognition import FacialRecognition
            facial_system = FacialRecognition()
            recognized = facial_system.recognize_faces()
            if recognized:
                print(f"\nEmma: Welcome, {recognized}! 🎉\n")
            else:
                print("Emma: Could not recognize face. Try registering first!\n")
        except ImportError:
            print("Emma: Face recognition not available. Install with:\n")
            print("pip install opencv-python face-recognition pillow numpy\n")
        except Exception as e:
            print(f"Emma: Error during recognition: {str(e)}\n")

    def show_registered_faces(self):
        """Show registered faces"""
        try:
            from brain.facial_recognition import FacialRecognition
            facial_system = FacialRecognition()
            facial_system.show_face_stats()
        except ImportError:
            print("Emma: Face recognition not available.\n")
        except Exception as e:
            print(f"Emma: Error: {str(e)}\n")

    def check_emails(self, task_manager):
        """Check and display email summary"""
        try:
            from skills.email_manager import EmailManager
            email_manager = EmailManager()
            
            counts = email_manager.get_all_unread_count()
            
            print("\n" + "=" * 50)
            print("📧 Email Check")
            print("=" * 50)
            print(f"\nTotal unread emails: {counts['total']}")
            
            if counts['gmail'] > 0:
                print(f"  Gmail: {counts['gmail']} unread")
            if counts['outlook'] > 0:
                print(f"  Outlook: {counts['outlook']} unread")
            
            if counts['total'] > 0:
                print("\n🔝 Important Emails:")
                important = email_manager.get_important_emails(limit=5)
                for i, email in enumerate(important, 1):
                    print(f"\n{i}. {email.get('subject', 'No Subject')}")
                    print(f"   From: {email.get('from', 'Unknown')}")
                    print(f"   Preview: {email.get('snippet', '')[:60]}...")
            
            print("\n" + "=" * 50 + "\n")
            
        except ImportError:
            print("Emma: Email integration not available. Run:\n")
            print("pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client O365\n")
        except Exception as e:
            print(f"Emma: Error checking emails: {str(e)}\n")

    def show_email_summary(self):
        """Show email summary"""
        try:
            from skills.email_manager import EmailManager
            email_manager = EmailManager()
            summary = email_manager.get_email_summary()
            print(f"\nEmma: {summary}\n")
        except ImportError:
            print("Emma: Email integration not available.\n")
        except Exception as e:
            print(f"Emma: Error: {str(e)}\n")

    def search_emails(self, keyword):
        """Search emails by keyword"""
        if not keyword:
            print("Emma: Please provide a search keyword.\n")
            return
        
        try:
            from skills.email_manager import EmailManager
            email_manager = EmailManager()
            results = email_manager.search_emails(keyword, limit=10)
            
            print("\n" + "=" * 50)
            print(f"📧 Search Results for '{keyword}'")
            print("=" * 50)
            
            if not results:
                print("No emails found.\n")
            else:
                for i, email in enumerate(results, 1):
                    print(f"\n{i}. {email.get('subject', 'No Subject')}")
                    print(f"   From: {email.get('from', 'Unknown')}")
                    print(f"   Source: {email.get('source', 'Unknown').upper()}")
                    print(f"   Preview: {email.get('snippet', '')[:60]}...")
            
            print("\n" + "=" * 50 + "\n")
            
        except ImportError:
            print("Emma: Email integration not available.\n")
        except Exception as e:
            print(f"Emma: Error searching emails: {str(e)}\n")

    def show_emails_from(self, sender):
        """Show emails from specific sender"""
        if not sender:
            print("Emma: Please provide a sender name.\n")
            return
        
        try:
            from skills.email_manager import EmailManager
            email_manager = EmailManager()
            emails = email_manager.get_emails_by_sender(sender, limit=10)
            
            print("\n" + "=" * 50)
            print(f"📧 Emails from '{sender}'")
            print("=" * 50)
            
            if not emails:
                print("No emails found from this sender.\n")
            else:
                for i, email in enumerate(emails, 1):
                    print(f"\n{i}. {email.get('subject', 'No Subject')}")
                    print(f"   Date: {email.get('date', 'Unknown')}")
                    print(f"   Preview: {email.get('snippet', '')[:60]}...")
            
            print("\n" + "=" * 50 + "\n")
            
        except ImportError:
            print("Emma: Email integration not available.\n")
        except Exception as e:
            print(f"Emma: Error: {str(e)}\n")

    def show_email_stats(self):
        """Show email statistics"""
        try:
            from skills.email_manager import EmailManager
            email_manager = EmailManager()
            stats = email_manager.get_stats()
            
            print("\n" + "=" * 50)
            print("📊 Email Statistics")
            print("=" * 50)
            print(f"Total emails checked: {stats['total_emails_checked']}")
            print(f"Tasks created from emails: {stats['total_tasks_created']}")
            print(f"Last check: {stats['last_check'] or 'Never'}")
            print(f"\nEmail sources:")
            print(f"  Gmail: {stats['sources'].get('gmail', 0)}")
            print(f"  Outlook: {stats['sources'].get('outlook', 0)}")
            print("=" * 50 + "\n")
            
        except ImportError:
            print("Emma: Email integration not available.\n")
        except Exception as e:
            print(f"Emma: Error: {str(e)}\n")
