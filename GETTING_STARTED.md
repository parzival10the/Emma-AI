# 🚀 Getting Started with Emma

Welcome to Emma - your personal daily task manager AI! This guide will help you get started.

## Quick Start (30 seconds)

1. **Start Emma:**
   ```bash
   python main.py
   ```

2. **Add your first task:**
   ```
   You: add task Study Math | Studies | 2026-07-26
   Emma: ✅ Added 'Study Math' to your Studies tasks!
   ```

3. **Check your tasks:**
   ```
   You: list tasks
   ```

4. **Complete a task:**
   ```
   You: complete 1
   Emma: ✅ Great job! Task 'Study Math' completed!
   ```

## Common Tasks

### Add Different Types of Tasks

**Study Task:**
```
add task Complete Chapter 5 Reading | Studies | 2026-07-26
```

**Gym Task:**
```
add task 30 min cardio session | Gym | 2026-07-25
```

**Food Task:**
```
add task Meal prep for week | Food
```

**Messages Task:**
```
add task Reply to College Group | Messages
```

**Custom Task:**
```
add task Custom task name | Other
```

### Daily Routine

1. **Morning Check-in:**
   ```
   check
   ```
   Emma will show all pending tasks and motivate you!

2. **After completing tasks:**
   ```
   complete 1
   complete 2
   ```

3. **See your progress:**
   ```
   status
   ```

### Track Your Performance

1. **View Statistics:**
   ```
   stats
   ```
   See completion rates, active streaks, and more!

2. **Get Motivated:**
   ```
   motivation
   ```
   Get a personalized motivational message.

3. **Weekly Report:**
   ```
   weekly
   ```
   See your activity across the week.

4. **Daily Summary:**
   ```
   summary
   ```
   See what you accomplished today.

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `add task <title> \| <category> \| [deadline]` | Create new task | `add task Homework \| Studies \| 2026-07-26` |
| `list tasks` | View all pending tasks | `list tasks` |
| `complete <id>` | Mark task as done | `complete 1` |
| `check` | Daily check-in | `check` |
| `status` | Show progress summary | `status` |
| `stats` | View statistics | `stats` |
| `achievements` | View achievements | `achievements` |
| `motivation` | Get motivation | `motivation` |
| `summary` | Today's summary | `summary` |
| `weekly` | Weekly report | `weekly` |
| `help` | Show all commands | `help` |
| `quit` | Exit Emma | `quit` |

## File Structure

Emma stores everything locally:

```
Emma-AI/
├── data/
│   ├── tasks.json           # Your task list
│   ├── emma_config.json     # Configuration
│   └── schedules.json       # Reminder settings
├── memory/
│   ├── user_memory.json     # Your preferences & habits
│   └── conversations.jsonl  # Conversation history
├── logs/
│   ├── activity.jsonl       # Activity log
│   └── statistics.json      # Performance stats
```

**All your data is stored locally - nothing goes to the cloud!** 🔒

## Tips for Success

1. **Be Consistent:** Use Emma daily for best results
2. **Set Realistic Deadlines:** Give yourself enough time to complete tasks
3. **Check Daily:** Use the `check` command in the morning
4. **Build Streaks:** Try to maintain streaks in different categories
5. **Review Progress:** Check `status` and `stats` weekly

## Understanding Streaks

Emma tracks your consistency:

- **Active Streak:** Consecutive days you complete at least one task in a category
- **View Your Streaks:** When you run `stats`, you'll see:
  ```
  Active Streaks: {'Studies': 5, 'Gym': 3}
  ```

## Customizing Emma

Edit `data/emma_config.json` to change:

- **Reminder times** (morning, noon, evening)
- **Your name** (Emma calls you by this)
- **Task categories** (add custom ones)

Example:
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

## Troubleshooting

**Q: Emma won't start**
- Make sure Python 3.8+ is installed
- Check you're in the Emma-AI directory

**Q: My tasks disappeared**
- Check `data/tasks.json` exists
- Your tasks are automatically saved in JSON format

**Q: Can't see emoji characters**
- Emma automatically handles this
- If you see errors, try running: `set PYTHONIOENCODING=utf-8`

**Q: How do I backup my data?**
- Copy the `data/` and `memory/` folders
- Or commit them to git!

## Next Steps

1. ✅ Add your first task
2. ✅ Complete a task
3. ✅ Check your daily summary
4. ✅ View your statistics
5. ✅ Build a streak!

## Questions?

Check the main **README.md** for more detailed information about features and architecture.

Happy task managing! 🎯

---

*Emma: "You've got this! I believe in you! 💪"*
