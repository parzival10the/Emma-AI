# 🤖 Emma - Your Daily Task Manager AI

Emma is an intelligent AI assistant designed to help you manage your daily tasks across multiple categories: **Studies**, **Messages**, **Gym**, **Food**, and more. Emma recognizes you through **facial recognition**, runs on **desktop and mobile**, and provides constant motivation and support.

## ✨ Features

### 📚 Task Management
- Organize tasks by Studies, Messages, Gym, Food, and custom categories
- Set deadlines and priorities
- Track completion progress
- View detailed statistics and analytics

### 🔔 Smart Reminders
- Receive check-ins at morning, noon, and evening (customizable)
- Daily summaries and weekly reports
- Personalized motivation based on performance

### 💬 Conversational AI
- Chat naturally with Emma about your tasks
- Get context-aware responses
- Emma learns your patterns and preferences

### 🧠 Memory System
- Emma learns your habits and preferences
- Maintains streaks for different categories
- Records achievements and milestones
- Provides personalized greetings

### 📊 Analytics
- Track completion rates
- View streak lengths by category
- Weekly activity reports
- Productivity insights

### 👤 **NEW!** Facial Recognition
- Register your face for secure login
- Automatic face recognition on startup
- Emma greets you by name
- Track recognition history

### 📱 **NEW!** Mobile App
- React Native app for iOS & Android
- Sync tasks across devices
- Access Emma on the go
- Same features as desktop version

### 🌐 API Server
- REST API for mobile apps
- Real-time data sync
- Cross-device synchronization

### 📧 **NEW!** Email Integration
- Check Gmail and Outlook emails
- See unread email counts
- Get important emails highlighted
- Search emails by keyword
- Filter emails by sender
- View email statistics
- API endpoints for mobile access

## 🚀 Quick Start

### Option 1: Desktop Only

```bash
# Install dependencies
pip install -r requirements.txt

# Run Emma
python main.py

# Use Emma normally
```

### Option 2: Desktop + Facial Recognition

```bash
# Install facial recognition
pip install opencv-python face-recognition

# Run Emma
python main.py

# Register your face
register face

# Next time, Emma recognizes you automatically
```

### Option 3: Desktop + Mobile

```bash
# Terminal 1: Start API server
python api_server.py

# Terminal 2: Start Emma
python main.py

# Terminal 3: Start mobile app
cd EmmaAIMobile
react-native run-android  # or run-ios
```

## 📖 How to Use

### Basic Commands

| Command | Description |
|---------|-------------|
| `add task <title> \| <category> \| [deadline]` | Add a new task |
| `list tasks` | Show all tasks |
| `complete <id>` | Mark task as done |
| `check` | Daily check-in |
| `status` | View progress |
| `stats` | View statistics |
| `check emails` | Check unread emails |
| `email summary` | Get email summary |
| `search emails <keyword>` | Search emails |
| `emails from <sender>` | Get emails from sender |
| `email stats` | View email statistics |
| `register face` | Register your face |
| `recognize` | Recognize your face |
| `faces` | Show registered faces |
| `help` | Show all commands |

### Examples

```
You: add task Study for Physics | Studies | 2026-07-28
Emma: ✅ Added 'Study for Physics' to your Studies tasks!

You: complete 1
Emma: ✅ Great job! Task completed!

You: check
Emma: [Shows daily check-in with pending tasks]

You: register face
Emma: [Opens camera for face registration]
```

## 📁 Project Structure

```
Emma-AI/
├── brain/
│   ├── emma.py                    # Core AI logic
│   └── facial_recognition.py      # Face recognition system
├── skills/
│   ├── task_manager.py           # Task management
│   └── scheduler.py              # Scheduling & reminders
├── memory/
│   ├── memory.py                 # Learning system
│   ├── user_memory.json          # User data
│   └── conversations.jsonl       # Conversation history
├── logs/
│   ├── logger.py                 # Activity logging
│   └── activity.jsonl            # Activity log
├── data/
│   ├── tasks.json                # Task database
│   ├── faces/                    # Facial data
│   └── emma_config.json          # Configuration
├── main.py                       # Desktop entry point
├── api_server.py                 # Mobile API server
├── EmmaAIMobile/                 # React Native mobile app
├── README.md                     # This file
├── GETTING_STARTED.md            # Quick start guide
├── FACIAL_RECOGNITION_SETUP.md   # Face recognition setup
├── MOBILE_APP_SETUP.md           # Mobile app setup
└── PROJECT_SUMMARY.md            # Detailed summary
```

## 🔐 Facial Recognition Features

### Register Your Face
```
You: register face
```
- Captures 5 photos of your face
- Creates a facial profile
- Stores securely on your computer

### Automatic Login
- Emma recognizes you on startup
- Logs you in automatically
- Shows personalized greeting

### View Statistics
```
You: faces
```
- Shows all registered users
- Displays recognition history
- Shows confidence scores

## 📱 Mobile App Features

### Screens
- **Home**: Dashboard with daily summary
- **Tasks**: Full task list with filters
- **Stats**: Productivity statistics
- **Face**: Face recognition login
- **Settings**: App preferences

### Synchronization
- All tasks sync automatically
- Works offline with local caching
- Real-time updates when online
- Cross-device task management

## 🛠️ Installation

### Desktop Version

```bash
# Clone repository
git clone <repo-url>
cd Emma-AI

# Install dependencies (optional for core features)
pip install -r requirements.txt

# Run Emma
python main.py
```

**No external dependencies required for basic features!**

### Mobile Version

See `MOBILE_APP_SETUP.md` for detailed React Native setup.

### Facial Recognition

See `FACIAL_RECOGNITION_SETUP.md` for detailed setup.

### Email Integration

See `EMAIL_INTEGRATION_SETUP.md` for detailed setup.

**Quick Setup:**
```bash
# Install email libraries
pip install -r requirements.txt

# Run Emma and check emails
python main.py
check emails
```

## 💾 Data Storage

- All data stored **locally** on your computer
- No cloud uploads or external APIs
- **Privacy-first design**
- Export/backup your data anytime

### Data Files
- `data/tasks.json` - Your tasks
- `data/faces/` - Facial recognition data
- `memory/user_memory.json` - Your preferences
- `logs/activity.jsonl` - Activity log

## 🎯 Task Categories

- **📚 Studies**: Assignments, exams, projects
- **📱 Messages**: Communications, follow-ups
- **💪 Gym**: Fitness, workouts
- **🍔 Food**: Meals, nutrition, groceries
- **✨ Other**: Custom tasks

## ⏰ Customization

Edit `data/emma_config.json`:

```json
{
  "creator": "Your Name",
  "reminders": {
    "morning": "07:00",
    "noon": "12:00",
    "evening": "18:00"
  },
  "categories": ["Studies", "Messages", "Gym", "Food", "Work", "Other"]
}
```

## 🔄 API Endpoints

The mobile app connects via REST API:

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PUT /api/tasks/:id/complete` - Mark complete
- `GET /api/stats` - Get statistics
- `GET /api/health` - Health check

## 🚀 Advanced Features

### Streaks
- Track consecutive days of task completion
- Build streaks in different categories
- Get rewards for consistency

### Analytics
- Completion rate tracking
- Category-wise breakdown
- Weekly/daily reports
- Productivity insights

### Memory System
- Emma learns your habits
- Personalized recommendations
- Achievement tracking
- Preference learning

## 📊 Technology Stack

- **Language**: Python 3.8+
- **Mobile**: React Native (iOS & Android)
- **API**: Flask with CORS
- **Storage**: JSON (local files)
- **Face Recognition**: OpenCV + face-recognition library
- **Dependencies**: Minimal (all optional)

## 🎓 Learning Resources

- `GETTING_STARTED.md` - Quick start guide (5 minutes)
- `FACIAL_RECOGNITION_SETUP.md` - Face recognition setup
- `MOBILE_APP_SETUP.md` - Mobile app development guide
- `PROJECT_SUMMARY.md` - Detailed technical overview

## 🤝 Support

- Check documentation files for setup help
- Look at `data/` directory structure
- Review logs in `logs/` for debugging
- Check error messages for guidance

## 🎁 What You Get

✅ Desktop task manager  
✅ Mobile iOS & Android app  
✅ Facial recognition login  
✅ Automatic synchronization  
✅ Beautiful analytics  
✅ Privacy-first design  
✅ Zero cloud dependency  
✅ Fully customizable  
✅ Well-documented  
✅ Easy to extend  

## 📈 Future Enhancements

- 🎤 Voice commands
- 📧 Email integration
- 🔗 Calendar sync
- 👥 Team collaboration
- ☁️ Cloud backup
- 🎮 Gamification

## 💡 Pro Tips

1. **Register face in good lighting** for better accuracy
2. **Check daily** to build streaks
3. **Use consistent categories** for better insights
4. **Keep phone nearby** for mobile notifications
5. **Review stats weekly** to track progress

## 🔒 Privacy & Security

- ✅ All data stored locally
- ✅ No cloud uploads
- ✅ No tracking or analytics
- ✅ No external APIs (except optional)
- ✅ Complete data control

## 📄 License

Created by Parzival for personal task management.

## 🎉 Summary

**Emma is your complete AI task manager:**

- 🖥️ **Desktop App** - Full-featured task management
- 📱 **Mobile App** - iOS & Android access
- 👤 **Face Recognition** - Secure login
- 🧠 **Smart AI** - Learns and adapts
- 📊 **Analytics** - Detailed insights
- 💾 **Privacy** - Everything local

Start using Emma today! 🚀

---

*Built with ❤️ for productivity and motivation*

**Version**: 2.1 (Desktop + Mobile + Facial Recognition)  
**Creator**: Parzival  
**Status**: ✅ Production Ready


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
