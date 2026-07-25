# 📸 Emma AI - Facial Recognition & Mobile Setup

## Quick Start

### 1. Install Facial Recognition Dependencies

```bash
pip install opencv-python face-recognition pillow numpy flask flask-cors
```

### 2. Register Your Face

```bash
python main.py
```

Then in Emma's chat:
```
You: register face
```

Emma will open your camera and ask you to capture 5 photos of your face from different angles.

### 3. Login with Face Recognition

On next startup, Emma will automatically try to recognize your face!

```
You: recognize
```

---

## 🎥 Facial Recognition Features

### Register Face
- **Command**: `register face`
- **What it does**: Captures 5 photos of your face and creates a facial profile
- **Time**: ~1 minute
- **Requirements**: Webcam, good lighting

### Recognize Face
- **Command**: `recognize`
- **What it does**: Scans your camera for your face and logs you in automatically
- **Time**: ~5 seconds
- **Accuracy**: ~95%

### View Face Stats
- **Command**: `faces`
- **What it does**: Shows all registered users and recognition history

### Automatic Login
- When Emma starts, she automatically tries to recognize your face
- If recognized, you're logged in immediately
- If not recognized, she asks for manual login

---

## 📱 Mobile App Setup

### Step 1: Install Node.js & React Native

```bash
# Install Node.js from https://nodejs.org/
# Then install React Native CLI

npm install -g react-native-cli
```

### Step 2: Create Mobile Project

```bash
cd Emma-AI
npx react-native init EmmaAIMobile
cd EmmaAIMobile
```

### Step 3: Install Dependencies

```bash
npm install @react-navigation/native @react-navigation/bottom-tabs react-native-screens react-native-safe-area-context
npm install axios moment react-native-vector-icons
npm install @react-native-community/async-storage
```

### Step 4: Copy App Files

Copy the screen files from the `MOBILE_APP_SETUP.md` into:
- `src/screens/` - Screen components
- `src/services/` - API client
- `src/components/` - Reusable components

### Step 5: Start API Server

In a **new terminal** in the Emma-AI directory:

```bash
pip install flask flask-cors
python api_server.py
```

You'll see:
```
🚀 Emma AI API Server
===================
Version: 2.1
Starting server on http://0.0.0.0:5000
📱 Mobile App can connect at: http://<your-ip>:5000
```

### Step 6: Run Mobile App

**Find your desktop IP:**
- Windows: `ipconfig` (look for IPv4 Address)
- Mac/Linux: `ifconfig`

**Update mobile app's API URL** in `src/services/api.js`:
```javascript
const API_URL = 'http://192.168.X.X:5000/api';  // Use your IP
```

**Run the app:**
```bash
# For Android
react-native run-android

# For iOS
react-native run-ios
```

---

## 🔧 Troubleshooting

### Facial Recognition Issues

**Q: "No face detected" error**
- Solution: Ensure good lighting, face clearly visible
- Try moving closer to camera
- Remove glasses or hats

**Q: "Could not load face encoding" error**
- Solution: Reinstall face-recognition:
```bash
pip uninstall face-recognition
pip install face-recognition
```

**Q: Camera window won't open**
- Solution: Check camera permissions
- Try: `pip install pillow`
- On Windows, ensure webcam is not used by another app

### Mobile App Issues

**Q: App crashes on startup**
- Solution: `npm install` then `npm start -- --reset-cache`

**Q: Cannot connect to desktop API**
- Solution: 
  - Ensure desktop API server is running (`python api_server.py`)
  - Use correct desktop IP address
  - Both devices must be on same WiFi network
  - Check Windows/Mac firewall allows port 5000

**Q: Tasks not syncing**
- Solution:
  - Restart both apps
  - Check API server is running
  - Verify network connection

---

## 📋 API Endpoints

### Health Check
```
GET /api/health
Response: { "status": "online", "version": "2.1" }
```

### Get All Tasks
```
GET /api/tasks
Response: [{ id, title, category, completed, ... }]
```

### Create Task
```
POST /api/tasks
Body: { "title": "Study", "category": "Studies", "deadline": "2026-07-28" }
```

### Complete Task
```
PUT /api/tasks/:id/complete
Response: { "completed": true, "completed_at": "..." }
```

### Get Statistics
```
GET /api/stats
Response: { "total": 10, "completed": 5, "pending": 5, "completion_rate": 50 }
```

---

## 🎯 Usage Examples

### Desktop (with Face Recognition)

```bash
# Start Emma
python main.py

# Register your face (first time)
Emma: I don't recognize you. Please register your face.
You: register face

# Next time, automatic login
Emma: ✅ Welcome back, Parzival! 🎉

# Use normally
You: add task Study Math | Studies | 2026-07-28
You: list tasks
You: complete 1
```

### Mobile App

- **Home Tab**: Dashboard with today's tasks and progress
- **Tasks Tab**: Full task list with filters
- **Stats Tab**: Productivity statistics
- **Face Tab**: (Future) Facial recognition on mobile
- **Settings Tab**: App preferences

### Syncing Between Desktop & Mobile

1. Both apps connect to the same API server
2. Tasks are stored in `data/tasks.json`
3. Changes sync automatically
4. Works offline - syncs when online

---

## 🚀 Running Both Desktop & Mobile

**Terminal 1 - API Server:**
```bash
python api_server.py
# Server running on port 5000
```

**Terminal 2 - Desktop Emma:**
```bash
python main.py
# Emma running with facial recognition
```

**Terminal 3 - Mobile App:**
```bash
cd EmmaAIMobile
react-native run-android  # or run-ios
```

Now you have:
- ✅ Desktop Emma with face login
- ✅ Mobile Emma on your phone
- ✅ All data synced automatically

---

## 📊 What Each Component Does

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **main.py** | Emma AI core | Python |
| **brain/facial_recognition.py** | Face detection & login | OpenCV + face-recognition |
| **api_server.py** | Mobile sync | Flask |
| **EmmaAIMobile/** | Mobile app | React Native |
| **data/faces/** | Facial data | Pickle files |

---

## 💡 Pro Tips

1. **Better facial recognition**: Register face in different lighting
2. **Fast sync**: Keep phone & desktop on same network
3. **Battery saving**: Mobile app uses local storage for offline use
4. **Security**: All face data stored locally, never uploaded

---

## 📞 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Face not recognized | Register face again with better lighting |
| Mobile app offline | Close and restart, or check WiFi |
| API server won't start | Check port 5000 is free: `lsof -i :5000` |
| Webcam locked | Close other apps using camera |
| Mobile app slow | Use WiFi instead of mobile data |

---

## 🎓 Next Level Features

Once everything is working:

1. **Push Notifications**: Get alerts on mobile
2. **Voice Commands**: "Hey Emma, add task..."
3. **Calendar Sync**: Auto-sync with Google Calendar
4. **Team Mode**: Share tasks with friends
5. **Cloud Backup**: Backup to cloud storage

---

## 📱 Mobile App Architecture

```
EmmaAIMobile/
├── App.js                          # Entry point
├── src/
│   ├── screens/                    # Tab screens
│   │   ├── HomeScreen.js
│   │   ├── TasksScreen.js
│   │   ├── StatsScreen.js
│   │   ├── FaceScreen.js
│   │   └── SettingsScreen.js
│   ├── services/
│   │   ├── api.js                 # Communicates with Flask server
│   │   └── storage.js             # Local storage
│   └── components/                 # Reusable UI
│       ├── TaskCard.js
│       ├── StatCard.js
│       └── StreakCard.js
└── package.json
```

---

**Emma is now ready for desktop + mobile use! 🚀✨**

*Questions? Check the main README.md and MOBILE_APP_SETUP.md*
