# 🤖 Emma - Your Daily Task Manager AI

Emma is an intelligent AI assistant designed to help you manage your daily tasks across multiple categories: **Studies**, **Messages**, **Gym**, **Food**, and more. Emma constantly monitors your commitments, reminds you proactively, and provides motivational support throughout your day.

## ✨ Features

- **📚 Task Categories**: Organize tasks by Studies, Messages, Gym, Food, and custom categories
- **🔔 Smart Reminders**: Receive check-ins at morning, noon, and evening (or custom times)
- **💾 Persistent Storage**: All tasks and preferences are saved automatically
- **🧠 Memory System**: Emma learns your habits, preferences, and patterns
- **📊 Analytics**: Track your productivity with detailed statistics and reports
- **🎯 Streak Tracking**: Build and maintain streaks for your daily tasks
- **💬 Conversational AI**: Chat naturally with Emma about your tasks and goals
- **🎭 Personalized Greetings**: Get context-aware greetings based on time and streaks

## 🚀 Quick Start

### Installation

1. Make sure you have Python 3.8+ installed
2. Clone the repository:
```bash
git clone <repository-url>
cd Emma-AI
```

3. Run Emma:
```bash
python main.py
```

## 📖 How to Use

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add task <title> \| <category> \| [deadline]` | Add a new task | `add task Complete Math Homework \| Studies \| 2026-07-28` |
| `list tasks` | Show all pending tasks | `list tasks` |
| `complete <task_id>` | Mark a task as completed | `complete 1` |
| `check` | Perform daily check-in | `check` |
| `status` | Show progress summary | `status` |
| `help` | Show all commands | `help` |
| `quit` | Exit Emma | `quit` |

### Examples

**Add a task:**
```
You: add task Gym workout | Gym | 2026-07-25
Emma: ✅ Added 'Gym workout' to your Gym tasks!
```

**Complete a task:**
```
You: complete 1
Emma: ✅ Great job! Task 'Complete Math Homework' completed!
```

**Daily check-in:**
```
You: check
Emma: [Shows pending tasks and provides motivation]
```

**View your progress:**
```
You: status
Emma: [Shows total tasks, completion rate, and breakdown by category]
```

## 📁 Project Structure

```
Emma-AI/
├── brain/
│   └── emma.py                 # Core Emma AI logic and conversation engine
├── skills/
│   ├── task_manager.py        # Task creation and management
│   └── scheduler.py           # Scheduling and reminders
├── memory/
│   ├── memory.py              # User preferences and habits tracking
│   ├── user_memory.json       # Stored user data
│   └── conversations.jsonl    # Conversation history
├── logs/
│   ├── logger.py              # Activity logging
│   ├── activity.jsonl         # Activity log
│   └── statistics.json        # Usage statistics
├── data/
│   ├── tasks.json             # All tasks database
│   ├── schedules.json         # Reminder schedules
│   └── emma_config.json       # Configuration
├── main.py                    # Entry point
└── README.md                  # This file
```

## 🎯 Task Categories

Emma supports the following task categories:

- **📚 Studies**: Academic assignments, projects, exams, reading
- **📱 Messages**: Important communications, follow-ups, emails
- **💪 Gym**: Fitness goals, workout sessions, health activities
- **🍔 Food**: Meal planning, nutrition, cooking, groceries
- **✨ Other**: Any custom tasks you want to track

## ⏰ Reminder Schedule

By default, Emma checks on you at:

- **🌅 Morning**: 07:00
- **☀️ Noon**: 12:00
- **🌙 Evening**: 18:00

You can customize these times in the configuration.

## 💾 Data Storage

Emma stores everything locally in JSON files:

- **tasks.json**: Your task list
- **user_memory.json**: Your preferences and habits
- **conversations.jsonl**: Conversation history (for learning)
- **activity.jsonl**: Activity log
- **statistics.json**: Productivity statistics

## 🔧 Configuration

Edit `data/emma_config.json` to customize:

```json
{
  "creator": "Parzival",
  "reminders": {
    "morning": "07:00",
    "noon": "12:00",
    "evening": "18:00"
  },
  "personality": "helpful, caring, motivating",
  "categories": ["Studies", "Messages", "Gym", "Food", "Other"]
}
```

## 📊 Tracking & Analytics

Emma tracks:

- **Completion Rate**: Percentage of tasks completed
- **Streaks**: Consecutive days of task completion
- **Habits**: Your patterns and preferences
- **Achievements**: Milestones and accomplishments
- **Weekly Reports**: Activity breakdown by day

View your statistics anytime with the `status` command.

## 🧠 How Emma Learns

Emma learns from your usage:

- **Preferences**: Your favorite study times, gym frequency, meal times
- **Habits**: How often you complete tasks, your productivity patterns
- **Streaks**: Your consistency in different task categories
- **Communication**: Your interaction style and preferences

This helps Emma provide increasingly personalized support.

## 🎭 Personalization

Emma's responses adapt based on:

- **Time of Day**: Different greetings and reminders (morning/noon/evening)
- **Your Streaks**: Celebrates your consistency
- **Task Urgency**: Emphasizes overdue tasks
- **Your Habits**: Learns and adapts to your patterns

## 🚀 Future Features

- 🎤 **Voice Integration**: Voice commands and speech-to-text
- 📱 **Mobile App**: Use Emma on your phone
- 📧 **Email Integration**: Sync tasks with email
- 🔗 **Calendar Sync**: Integrate with your calendar
- 🤝 **Team Mode**: Share tasks and collaborate
- 🌐 **Cloud Sync**: Sync across devices
- 🎨 **Dark Mode**: UI improvements
- 📈 **Advanced Analytics**: Machine learning insights

## 🛠️ Development

### Running Tests

(Coming soon)

### Contributing

Feel free to submit issues and pull requests!

## 📝 License

This project is created by Parzival for personal use. Feel free to modify and use as needed.

## 💡 Tips

1. **Daily Check-ins**: Make it a habit to check in with Emma daily for best results
2. **Realistic Deadlines**: Set achievable deadlines to build momentum
3. **Consistency**: The more you use Emma, the better she learns your patterns
4. **Categories**: Use the right category for each task for better organization
5. **Regular Reviews**: Check your statistics weekly to see your progress

## 🙋 Support

For issues or questions, you can:
- Check the README
- Look at the `data/` and `memory/` folders to understand your data
- Customize settings in `emma_config.json`

---

**Happy task managing with Emma! 🌟**

*Built with ❤️ for productivity and motivation*
