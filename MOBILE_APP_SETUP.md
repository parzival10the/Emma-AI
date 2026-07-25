# 📱 Emma AI Mobile App - React Native Setup Guide

## Overview

Emma now has a full-featured React Native mobile app for iOS and Android! This guide will help you set up and run the mobile app.

## Prerequisites

### Required
- **Node.js** 14.0+ (https://nodejs.org/)
- **npm** or **yarn**
- **React Native CLI**: `npm install -g react-native-cli`
- **Watchman** (Mac/Linux): `brew install watchman`

### Platform-Specific
**For iOS:**
- Xcode 12+ (Mac only)
- CocoaPods

**For Android:**
- Android Studio
- Android SDK 21+
- Java Development Kit (JDK) 8+

## Installation

### 1. Create React Native Project

```bash
# Navigate to Emma-AI directory
cd Emma-AI

# Create the mobile app
npx react-native init EmmaAIMobile

cd EmmaAIMobile
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install

# Install additional Emma AI dependencies
npm install @react-navigation/native @react-navigation/bottom-tabs react-native-screens react-native-safe-area-context
npm install axios moment react-native-vector-icons
npm install @react-native-community/async-storage
```

### 3. Link Native Modules

```bash
npx react-native link
```

## Project Structure

```
EmmaAIMobile/
├── App.js                          # Main app entry
├── src/
│   ├── screens/
│   │   ├── HomeScreen.js          # Dashboard
│   │   ├── TasksScreen.js         # Task management
│   │   ├── AddTaskScreen.js       # Add new task
│   │   ├── StatsScreen.js         # Statistics
│   │   ├── FaceScreen.js          # Face recognition
│   │   └── SettingsScreen.js      # Settings
│   ├── components/
│   │   ├── TaskCard.js            # Task component
│   │   ├── CategoryFilter.js      # Category selector
│   │   └── StreakCard.js          # Streak display
│   ├── services/
│   │   ├── api.js                 # API communication with desktop
│   │   └── storage.js             # Local storage
│   ├── utils/
│   │   ├── categories.js          # Category definitions
│   │   └── colors.js              # Color scheme
│   └── navigation/
│       └── Navigation.js           # Navigation setup
└── package.json
```

## Creating the Mobile App Files

### 1. Main App Component (App.js)

```javascript
import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import TasksScreen from './src/screens/TasksScreen';
import StatsScreen from './src/screens/StatsScreen';
import FaceScreen from './src/screens/FaceScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;
            
            if (route.name === 'Home') iconName = 'home';
            else if (route.name === 'Tasks') iconName = 'clipboard-list';
            else if (route.name === 'Stats') iconName = 'chart-box';
            else if (route.name === 'Face') iconName = 'face-recognition';
            else if (route.name === 'Settings') iconName = 'cog';
            
            return <Icon name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#4CAF50',
          tabBarInactiveTintColor: '#999',
        })}
      >
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Tasks" component={TasksScreen} />
        <Tab.Screen name="Stats" component={StatsScreen} />
        <Tab.Screen name="Face" component={FaceScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

### 2. Home Screen (src/screens/HomeScreen.js)

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { API } from '../services/api';

export default function HomeScreen() {
  const [greeting, setGreeting] = useState('');
  const [stats, setStats] = useState({});
  const [pendingTasks, setPendingTasks] = useState([]);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await API.getTasks();
      const tasks = response.data;
      
      const pending = tasks.filter(t => !t.completed);
      setPendingTasks(pending.slice(0, 5));
      
      const completed = tasks.filter(t => t.completed).length;
      setStats({
        total: tasks.length,
        completed: completed,
        pending: pending.length,
      });
      
      const hour = new Date().getHours();
      if (hour < 12) setGreeting('Good Morning! 🌅');
      else if (hour < 18) setGreeting('Good Afternoon! ☀️');
      else setGreeting('Good Evening! 🌙');
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>{greeting}</Text>
        <Text style={styles.subtitle}>Emma AI Task Manager</Text>
      </View>

      <View style={styles.statsContainer}>
        <StatCard icon="checkbox-marked-circle" title="Completed" value={stats.completed} />
        <StatCard icon="progress-clock" title="Pending" value={stats.pending} />
        <StatCard icon="target" title="Total" value={stats.total} />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📋 Today's Tasks</Text>
        {pendingTasks.map((task) => (
          <TaskItemCard key={task.id} task={task} />
        ))}
      </View>

      <TouchableOpacity style={styles.fab}>
        <Icon name="plus" size={30} color="#fff" />
      </TouchableOpacity>
    </ScrollView>
  );
}

const StatCard = ({ icon, title, value }) => (
  <View style={styles.statCard}>
    <Icon name={icon} size={24} color="#4CAF50" />
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statTitle}>{title}</Text>
  </View>
);

const TaskItemCard = ({ task }) => (
  <View style={styles.taskCard}>
    <Text style={styles.taskTitle}>{task.title}</Text>
    <Text style={styles.taskCategory}>{task.category}</Text>
    {task.deadline && <Text style={styles.taskDeadline}>Due: {task.deadline}</Text>}
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#4CAF50',
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 10,
    marginTop: -30,
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    margin: 5,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    elevation: 3,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 5,
  },
  statTitle: {
    fontSize: 12,
    color: '#999',
    marginTop: 3,
  },
  section: {
    padding: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  taskCard: {
    backgroundColor: '#fff',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    elevation: 2,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  taskCategory: {
    fontSize: 12,
    color: '#4CAF50',
    marginTop: 5,
  },
  taskDeadline: {
    fontSize: 12,
    color: '#999',
    marginTop: 3,
  },
  fab: {
    position: 'absolute',
    bottom: 80,
    right: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 8,
  },
});
```

### 3. Tasks Screen (src/screens/TasksScreen.js)

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';
import { API } from '../services/api';

export default function TasksScreen({ navigation }) {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await API.getTasks();
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const completeTask = async (taskId) => {
    try {
      await API.completeTask(taskId);
      loadTasks();
    } catch (error) {
      console.error('Error completing task:', error);
    }
  };

  const filteredTasks = filter === 'all' 
    ? tasks 
    : tasks.filter(t => t.category === filter);

  const renderTask = ({ item }) => (
    <TouchableOpacity
      style={[styles.taskCard, item.completed && styles.completedTask]}
      onPress={() => completeTask(item.id)}
    >
      <Text style={styles.taskTitle}>{item.title}</Text>
      <View style={styles.taskFooter}>
        <Text style={styles.category}>{item.category}</Text>
        <Text style={styles.completed}>{item.completed ? '✅' : '⏳'}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={filteredTasks}
        renderItem={renderTask}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  listContainer: {
    padding: 15,
  },
  taskCard: {
    backgroundColor: '#fff',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    elevation: 2,
  },
  completedTask: {
    opacity: 0.6,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '600',
  },
  taskFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  category: {
    fontSize: 12,
    color: '#4CAF50',
  },
  completed: {
    fontSize: 14,
  },
});
```

## Running the App

### For Android

```bash
# Build and run on connected device or emulator
react-native run-android

# Or
npm run android
```

### For iOS

```bash
# Build and run on iOS simulator
react-native run-ios

# Or
npm run ios

# For specific device
react-native run-ios --device "iPhone 12"
```

## Desktop API Server Setup

The mobile app needs to communicate with the desktop Emma app. Create a simple Flask API:

### Create `api_server.py`

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

TASKS_FILE = "data/tasks.json"

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "category": data['category'],
        "deadline": data.get('deadline'),
        "completed": False
    }
    tasks.append(new_task)
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
    
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
    
    return jsonify({"status": "completed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Run the API

```bash
pip install flask flask-cors
python api_server.py
```

The API will be available at `http://localhost:5000`

## Configuration

Update `src/services/api.js` with your desktop IP:

```javascript
const API_URL = 'http://192.168.1.100:5000/api';  // Replace with your desktop IP

export const API = {
  async getTasks() {
    return fetch(`${API_URL}/tasks`).then(r => r.json());
  },
  
  async completeTask(id) {
    return fetch(`${API_URL}/tasks/${id}/complete`, { 
      method: 'PUT' 
    }).then(r => r.json());
  },
};
```

## Building for Distribution

### Android APK

```bash
cd android
./gradlew assembleRelease
# APK will be in android/app/build/outputs/apk/release/
```

### iOS IPA

```bash
cd ios
xcodebuild -workspace EmmaAIMobile.xcworkspace -scheme EmmaAIMobile -configuration Release -archivePath ~/Desktop/EmmaAI.xcarchive archive
xcodebuild -exportArchive -archivePath ~/Desktop/EmmaAI.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath ~/Desktop/
```

## Troubleshooting

**Q: App crashes on startup**
- Check that Node modules are installed: `npm install`
- Clear cache: `npm start -- --reset-cache`

**Q: Can't connect to desktop API**
- Ensure desktop app is running with API server
- Check your IP address is correct
- Both devices must be on same network

**Q: Face recognition not working on mobile**
- Install: `npm install react-native-camera expo-face-detector`
- Request camera permissions in `AndroidManifest.xml` and `Info.plist`

## Next Steps

1. ✅ Install React Native
2. ✅ Set up mobile project
3. ✅ Create screens
4. ✅ Connect to desktop API
5. ✅ Test on device
6. ✅ Build and distribute

---

**Emma AI Mobile** - Your task manager anywhere! 📱✨
