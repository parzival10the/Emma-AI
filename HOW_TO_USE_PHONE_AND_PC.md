# 📱💻 Emma AI - Complete Phone & PC Setup Guide

## Overview

Emma runs on:
- **PC/Desktop** (Windows, Mac, Linux) - Full task manager
- **Phone** (iPhone/Android) - Mobile app via React Native
- **Both sync automatically** via API server

---

## 🖥️ STEP 1: Setup Emma on PC (15 minutes)

### Step 1.1: Install Python
1. Download Python from https://www.python.org/
2. Install Python 3.8 or higher
3. Make sure "Add Python to PATH" is checked

### Step 1.2: Get Emma
1. Download or clone Emma-AI repository
2. Navigate to Emma-AI folder in terminal/command prompt

### Step 1.3: Install Dependencies
```bash
pip install -r requirements.txt
```

**What this installs:**
- opencv-python (for facial recognition)
- face-recognition (face detection)
- flask (API server)
- Other tools

### Step 1.4: Start Emma
```bash
python main.py
```

You'll see:
```
==================================================
 Emma AI - Daily Task Manager
==================================================
Version      : 2.1
Creator      : Parzival
Status       : ONLINE 🟢
==================================================

Good morning, Parzival!
Type 'help' for available commands or 'quit' to exit.

You:
```

**That's it!** Emma is running on your PC! ✅

---

## 📱 STEP 2: Setup Emma on Phone (30 minutes)

### Method A: Using Web Browser (Easiest - 5 minutes)

**If you don't want to install the full app:**

1. **On PC Terminal:**
   ```bash
   python api_server.py
   ```

2. **On Phone Browser:**
   - Visit: `http://<your-pc-ip>:5000/api/tasks`
   - You'll see your tasks in JSON format
   - Can use web dashboard (optional setup)

### Method B: Full React Native App (Best - 30 minutes)

#### Step 2.1: Install Node.js on PC
1. Download from https://nodejs.org/
2. Install Node.js (includes npm)
3. Verify: `node --version` and `npm --version`

#### Step 2.2: Create Mobile Project
```bash
# Navigate to Emma-AI folder
cd Emma-AI

# Create React Native project
npx react-native init EmmaAIMobile

# Go into the new project
cd EmmaAIMobile
```

#### Step 2.3: Install Mobile Dependencies
```bash
npm install @react-navigation/native @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install axios moment react-native-vector-icons
npm install @react-native-community/async-storage
```

#### Step 2.4: Set Up Your IP Address

**Find your PC's IP address:**

**Windows:**
1. Open Command Prompt
2. Type: `ipconfig`
3. Look for "IPv4 Address" (like 192.168.X.X)

**Mac/Linux:**
1. Open Terminal
2. Type: `ifconfig`
3. Look for inet address

**Your IP Example:** `192.168.1.100`

#### Step 2.5: Update Mobile App Configuration

In EmmaAIMobile folder, edit `src/services/api.js`:

```javascript
// Replace YOUR_IP with your actual IP
const API_URL = 'http://192.168.1.100:5000/api';

export const API = {
  async getTasks() {
    return fetch(`${API_URL}/tasks`).then(r => r.json());
  },
  
  async addTask(task) {
    return fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task)
    }).then(r => r.json());
  },
  
  async completeTask(id) {
    return fetch(`${API_URL}/tasks/${id}/complete`, {
      method: 'PUT'
    }).then(r => r.json());
  }
};
```

#### Step 2.6: Run Mobile App

**For Android:**
```bash
react-native run-android
```

**For iPhone:**
```bash
react-native run-ios
```

The app will build and open on your device/emulator.

---

## 🔄 STEP 3: Sync PC & Phone (5 minutes)

### Setup Synchronization

You need **3 terminal windows** open:

**Terminal 1 - API Server (Bridge between PC and Phone):**
```bash
cd Emma-AI
python api_server.py
```

Output:
```
🚀 Emma AI API Server
====================
Starting server on http://0.0.0.0:5000
```

**Terminal 2 - Desktop Emma:**
```bash
cd Emma-AI
python main.py
```

**Terminal 3 - Mobile App:**
```bash
cd EmmaAIMobile
react-native run-android  # or run-ios
```

✅ **Now everything is synced!**

---

## 📝 How to USE Emma

### Using Emma on PC

**Add a Task:**
```
You: add task Study Math | Studies | 2026-07-28
Emma: ✅ Added 'Study Math' to your Studies tasks!
```

**View Tasks:**
```
You: list tasks
```

Shows:
```
📚 Studies:
⏳ [1] Study Math
   Due: 2026-07-28
```

**Complete a Task:**
```
You: complete 1
Emma: ✅ Great job! Task 'Study Math' completed!
```

**Daily Check-in:**
```
You: check
```

Shows all pending tasks for the day.

**View Statistics:**
```
You: stats
```

Shows:
- Total tasks
- Completed tasks
- Completion rate
- Streaks by category

**Register Your Face (Optional):**
```
You: register face
```

Emma opens your camera and captures 5 photos of your face.

### Using Emma on Phone

**Tab 1: Home 🏠**
- Welcome message
- Today's statistics
- Top 5 pending tasks
- Quick add button (+)

**Tab 2: Tasks 📋**
- Full task list
- Filter by category
- Tap task to mark complete
- Swipe to delete

**Tab 3: Statistics 📊**
- Completion rate graph
- Tasks by category
- Total/Completed/Pending counts

**Tab 4: Face 👤**
- Facial recognition login
- Registered users
- Recognition history

**Tab 5: Settings ⚙️**
- App preferences
- Sync status
- About

---

## 🔄 Workflow Examples

### Example 1: Daily Morning Routine

**On PC:**
1. Start Emma: `python main.py`
2. Daily check: `check`
3. See all pending tasks
4. Add new tasks for the day

**On Phone:**
- Open Emma mobile app
- See same tasks synced
- Check morning statistics
- Motivate yourself!

### Example 2: Complete Task During Day

**On PC:**
```
You: add task Gym Session | Gym | 2026-07-25
Emma: ✅ Added 'Gym Session' to your Gym tasks!
```

**On Phone:**
- Open app
- Gym task automatically appears (synced!)
- Tap to mark complete

**On PC:**
- Sync happens automatically
- Task shows as completed

### Example 3: Evening Review

**On Phone:**
- Check today's summary
- View completion rate
- See streak progress

**On PC:**
```
You: summary
You: weekly
```

Shows all activity from the day and week.

---

## 📊 What Syncs Between Devices

✅ **Tasks** - Add, edit, delete on either device
✅ **Completion Status** - Mark complete on phone, shows on PC
✅ **Categories** - Studies, Gym, Food, Messages, Other
✅ **Deadlines** - Same on both
✅ **Priority** - Synced across devices
✅ **Statistics** - Always up-to-date

---

## 🔐 Network Requirements

Both devices need to be on **same WiFi network**.

**How to check:**
1. PC: Check WiFi name you're connected to
2. Phone: Check WiFi name you're connected to
3. Both should show same network name

**If different networks:**
- Use mobile hotspot from PC
- Or connect both to same WiFi

---

## 🛠️ Troubleshooting

### PC Setup Issues

**Q: Python not recognized**
- Solution: Reinstall Python with "Add to PATH" checked

**Q: pip install fails**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Q: Emma won't start**
```bash
# Clear cache
python -m pip install --force-reinstall -r requirements.txt
python main.py
```

### Phone Setup Issues

**Q: Mobile app won't run**
```bash
cd EmmaAIMobile
npm install  # reinstall dependencies
react-native run-android
```

**Q: Can't connect to PC API**
- Check IP address is correct
- Ensure API server is running: `python api_server.py`
- Both on same WiFi network
- Check firewall allows port 5000

**Q: Tasks not syncing**
- Verify API server is running
- Close and restart both apps
- Check network connection

### Facial Recognition Issues

**Q: Face recognition won't work**
```bash
pip uninstall face-recognition
pip install face-recognition==1.3.5
```

**Q: Camera won't open**
- Allow camera permission in privacy settings
- Close other apps using camera
- Restart Emma

---

## 📋 Complete Setup Checklist

### PC Setup
- [ ] Python 3.8+ installed
- [ ] Emma-AI downloaded
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Emma starts: `python main.py`
- [ ] Can add tasks
- [ ] Can complete tasks

### Phone Setup
- [ ] Node.js installed
- [ ] React Native project created
- [ ] npm dependencies installed
- [ ] IP address configured
- [ ] Mobile app runs: `react-native run-android`
- [ ] Can view tasks

### Sync Setup
- [ ] API server running: `python api_server.py`
- [ ] Desktop Emma running: `python main.py`
- [ ] Mobile app running
- [ ] Tasks visible on both
- [ ] Changes sync automatically

---

## 📱 Quick Reference - PC Terminal Commands

```bash
# Start Emma on PC
python main.py

# Start API server (for mobile sync)
python api_server.py

# Start mobile app
cd EmmaAIMobile
react-native run-android     # Android
react-native run-ios         # iPhone

# Stop any app
Press Ctrl+C
```

---

## 📱 Quick Reference - Phone App Navigation

```
Bottom Menu (5 Tabs):
🏠 Home          → Daily summary
📋 Tasks         → Full task list  
📊 Stats         → Statistics
👤 Face          → Face recognition
⚙️ Settings      → Preferences
```

---

## 🎯 Recommended Daily Use

### Morning (PC)
1. Start Emma: `python main.py`
2. Check: `type: check`
3. Add today's tasks
4. Get motivation: `type: motivation`

### Throughout Day (Phone)
1. Open Emma mobile app
2. View pending tasks
3. Complete tasks as you go
4. Check statistics

### Evening (PC or Phone)
1. Review the day: `type: summary`
2. Check completion rate: `type: stats`
3. Plan tomorrow

---

## 🔄 Syncing Details

**How it works:**
1. PC saves tasks to `data/tasks.json`
2. API server reads from this file
3. Mobile app requests from API server
4. Changes sync in real-time

**Files involved:**
```
PC:
  - data/tasks.json (main database)
  - api_server.py (serves data to phone)
  
Phone:
  - Connects to API at http://IP:5000
  - Shows and edits tasks
  - Changes go back to PC
```

---

## 💾 Backup Your Data

**Backup on PC:**
```bash
# Copy these folders to safe location
cp -r data backup_data
cp -r memory backup_memory
cp -r logs backup_logs
```

**Your data is safe:**
- Stored locally (not in cloud)
- Everything in `data/` folder
- Can backup anytime

---

## 🚀 Once Everything Works

### Next Steps
1. **Build streaks** - Complete tasks daily
2. **Register face** - `register face` on PC
3. **Get motivated** - Use mobile app for motivation
4. **Review weekly** - Check `weekly` command
5. **Customize** - Edit `data/emma_config.json`

### Customization
Edit `data/emma_config.json`:
```json
{
  "creator": "Your Name",
  "reminders": {
    "morning": "07:00",
    "noon": "12:00",
    "evening": "18:00"
  },
  "categories": ["Studies", "Messages", "Gym", "Food", "Work"]
}
```

---

## 📞 Support Resources

| Issue | Solution |
|-------|----------|
| Setup help | Read QUICK_START.md |
| PC commands | Type `help` in Emma |
| Mobile issues | Check MOBILE_APP_SETUP.md |
| Facial recognition | See FACIAL_RECOGNITION_SETUP.md |
| Tech details | Read PROJECT_SUMMARY.md |

---

## ✅ Verification Checklist

Once setup, verify:
- [ ] PC Emma works: `python main.py`
- [ ] Can add tasks: `add task Test | Other`
- [ ] Can complete: `complete 1`
- [ ] API server works: `python api_server.py`
- [ ] Phone app loads: `react-native run-android`
- [ ] Tasks sync: Add on PC, see on phone
- [ ] Changes sync: Complete on phone, see on PC

---

## 🎉 You're All Set!

You now have Emma running on:
- ✅ **PC/Desktop** - Full task manager
- ✅ **Phone** - Mobile access
- ✅ **Synced** - Everything synchronized
- ✅ **Facial Recognition** - Optional login (PC)

**Start using today!** 🚀

---

## 🆘 Emergency Help

**Something's not working?**

1. **PC won't start:**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

2. **Phone won't connect:**
   - Verify IP: `ipconfig` (Windows)
   - Check WiFi: Both on same network
   - Restart API: `python api_server.py`

3. **Data lost:**
   - Check `data/tasks.json` file
   - Restore from backup if available

4. **Sync not working:**
   - Ensure API server running
   - Check firewall
   - Verify IP address correct

---

**Emma AI v2.1** - Your Complete Task Manager 📱💻

*Now on your PC and Phone!*

✅ **Setup Complete**  
🎯 **Ready to Use**  
📊 **Stay Productive**

Start managing your tasks today! 🚀
