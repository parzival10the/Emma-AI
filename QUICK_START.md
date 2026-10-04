# 🚀 Emma AI v2.1 - Quick Installation & Setup

## ⏱️ Time Required
- **Desktop Only**: 5 minutes
- **Desktop + Face Recognition**: 10 minutes
- **Full Setup (Desktop + Mobile)**: 30 minutes

---

## 🖥️ Desktop Setup (5 min)

### Step 1: Install Python Dependencies
```bash
cd Emma-AI
pip install -r requirements.txt
```

### Step 2: Run Emma
```bash
python main.py
```

### Step 3: Start Using
```
You: add task Study Math | Studies | 2026-07-28
You: list tasks
You: complete 1
You: check
```

**That's it!** Emma is ready to use. 🎉

---

## 👤 Add Facial Recognition (10 min)

### Step 1: Install Face Recognition Libraries
```bash
pip install opencv-python face-recognition
```

### Step 2: Start Emma
```bash
python main.py
```

### Step 3: Register Your Face
```
You: register face
```

Follow the instructions:
- Face the camera
- Press SPACE to capture 5 photos
- Press Q to quit

### Step 4: Use Facial Login
- Next time you start Emma, she recognizes you automatically
- Or use: `You: recognize`

**Done!** You now have facial recognition. 🎉

---

## 📱 Mobile App Setup (30 min)

### Prerequisites
- Node.js installed (https://nodejs.org/)
- Android Studio or Xcode (for emulator)
- Desktop Emma running

### Step 1: Create Mobile Project
```bash
cd Emma-AI
npx react-native init EmmaAIMobile
cd EmmaAIMobile
```

### Step 2: Install Dependencies
```bash
npm install @react-navigation/native @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install axios moment react-native-vector-icons
npm install @react-native-community/async-storage
```

### Step 3: Add App Files

Copy these files to your React Native project:
- Screens to: `src/screens/`
- Services to: `src/services/`
- Components to: `src/components/`

(See MOBILE_APP_SETUP.md for exact code)

### Step 4: Update API Configuration

Edit `src/services/api.js`:
```javascript
// Get your desktop IP:
// Windows: ipconfig (look for IPv4)
// Mac/Linux: ifconfig

const API_URL = 'http://192.168.X.X:5000/api';  // Update with your IP
```

### Step 5: Start API Server

In a **new terminal** in Emma-AI directory:
```bash
python api_server.py
```

You'll see:
```
🚀 Emma AI API Server
====================
Starting server on http://0.0.0.0:5000
```

### Step 6: Run Mobile App

Back in EmmaAIMobile directory:

**For Android:**
```bash
react-native run-android
```

**For iOS:**
```bash
react-native run-ios
```

### Step 7: Enjoy!

Now you have:
- ✅ Desktop Emma on your computer
- ✅ Mobile Emma on your phone
- ✅ All data syncs automatically

---

## 🎯 Recommended Setup Order

### First Time User
1. ✅ Desktop Setup (5 min)
2. ✅ Add Facial Recognition (5 min)
3. ✅ Get comfortable with Emma (5 min)
4. ✅ Later: Add Mobile App (30 min)

### Power User
1. ✅ All of the above
2. ✅ Customize categories
3. ✅ Set reminder times
4. ✅ Build streaks

---

## 📋 Installation Checklist

### Desktop
- [ ] Cloned repository
- [ ] Installed Python 3.8+
- [ ] Installed requirements: `pip install -r requirements.txt`
- [ ] Ran `python main.py` successfully
- [ ] Added first task
- [ ] Used Emma for a day

### Face Recognition
- [ ] Installed opencv: `pip install opencv-python`
- [ ] Installed face-recognition: `pip install face-recognition`
- [ ] Registered face: `register face`
- [ ] Tested recognition: `recognize`
- [ ] Checked face stats: `faces`

### Mobile App
- [ ] Installed Node.js
- [ ] Created React Native project
- [ ] Installed npm dependencies
- [ ] Added app files
- [ ] Updated API URL
- [ ] Started API server
- [ ] Built and ran mobile app
- [ ] Synced tasks between devices

---

## 🐛 Troubleshooting

### Desktop Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Try reinstalling requirements
pip install -r requirements.txt --force-reinstall
```

### Face Recognition Not Working
```bash
# Reinstall with specific version
pip uninstall face-recognition
pip install face-recognition==1.3.0

# Check webcam access
# Windows: Check privacy settings
# Mac: Allow terminal camera access
```

### Mobile App Won't Connect
```bash
# Check API server is running
curl http://localhost:5000/api/health

# Verify IP address is correct
ipconfig  # Windows
ifconfig  # Mac/Linux

# Check firewall allows port 5000
```

---

## ✨ What to Try First

### As Soon as You Start
1. `add task Test Task | Other`
2. `list tasks`
3. `complete 1`
4. `status`

### Next Day
1. `check` - Daily check-in
2. `add task Study Math | Studies | 2026-07-26`
3. `stats` - See your progress

### First Week
1. `motivation` - Get inspired
2. `weekly` - See weekly summary
3. `register face` - Add facial recognition

### Later
1. Customize categories in config
2. Set optimal reminder times
3. Review achievements
4. Build streaks

---

## 🎓 Learning Resources

| Doc | Time | Topic |
|-----|------|-------|
| GETTING_STARTED.md | 5 min | Quick start |
| FACIAL_RECOGNITION_SETUP.md | 10 min | Face recognition |
| MOBILE_APP_SETUP.md | 20 min | Mobile development |
| README.md | 15 min | Complete guide |
| PROJECT_SUMMARY.md | 15 min | Technical details |
| VERSION_2.1_SUMMARY.md | 10 min | What's new |

---

## 💾 Data Backup

### Manual Backup
```bash
# Copy these folders to backup location
cp -r data/ backup_data/
cp -r memory/ backup_memory/
cp -r logs/ backup_logs/
```

### Restore from Backup
```bash
cp -r backup_data/* data/
cp -r backup_memory/* memory/
cp -r backup_logs/* logs/
```

---

## 🔄 Update Emma

### Get Latest Version
```bash
git pull origin main
pip install -r requirements.txt
```

### Preserve Your Data
Your data in `data/`, `memory/`, and `logs/` directories is automatically preserved during updates.

---

## 🎉 You're Ready!

You now have everything to get started with Emma AI v2.1!

```
🖥️  Desktop: python main.py
👤 Face: register face
📱 Mobile: npm start
🌐 API: python api_server.py
```

**Choose what works for you and start today!**

---

## 📞 Quick Reference

| Command | What it Does |
|---------|-------------|
| `python main.py` | Start desktop Emma |
| `python api_server.py` | Start API server |
| `react-native run-android` | Run mobile app |
| `register face` | Register your face |
| `add task X \| Y` | Add new task |
| `complete 1` | Mark task done |
| `check` | Daily check-in |
| `stats` | View statistics |

---

**Emma AI v2.1 - Ready to Transform Your Productivity! 🚀**

*Choose your setup and get started now!*
