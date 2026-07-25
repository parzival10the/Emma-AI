"""
Emma AI API Server
Provides REST API for mobile app and other clients
Run with: python api_server.py
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Data files
TASKS_FILE = "data/tasks.json"
CONFIG_FILE = "data/emma_config.json"
STATS_FILE = "logs/statistics.json"

# API version
API_VERSION = "2.1"


def load_tasks():
    """Load tasks from file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save tasks to file"""
    Path("data").mkdir(exist_ok=True)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


def load_config():
    """Load Emma config"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Emma AI API",
        "version": API_VERSION,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get Emma configuration"""
    config = load_config()
    return jsonify(config)


# ==================== TASK ENDPOINTS ====================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = load_tasks()
    return jsonify(tasks)


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get specific task"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create new task"""
    try:
        data = request.json
        tasks = load_tasks()
        
        new_task = {
            "id": max([t['id'] for t in tasks], default=0) + 1,
            "title": data.get('title', 'Untitled'),
            "category": data.get('category', 'Other'),
            "deadline": data.get('deadline'),
            "priority": data.get('priority', 'medium'),
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        tasks.append(new_task)
        save_tasks(tasks)
        
        return jsonify(new_task), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task"""
    try:
        data = request.json
        tasks = load_tasks()
        
        task = next((t for t in tasks if t['id'] == task_id), None)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        
        # Update fields
        if 'title' in data:
            task['title'] = data['title']
        if 'category' in data:
            task['category'] = data['category']
        if 'deadline' in data:
            task['deadline'] = data['deadline']
        if 'priority' in data:
            task['priority'] = data['priority']
        if 'completed' in data:
            task['completed'] = data['completed']
            if data['completed']:
                task['completed_at'] = datetime.now().isoformat()
        
        save_tasks(tasks)
        return jsonify(task)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task"""
    try:
        tasks = load_tasks()
        tasks = [t for t in tasks if t['id'] != task_id]
        save_tasks(tasks)
        
        return jsonify({"message": "Task deleted", "id": task_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    """Mark task as complete"""
    try:
        tasks = load_tasks()
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        
        task['completed'] = True
        task['completed_at'] = datetime.now().isoformat()
        
        save_tasks(tasks)
        return jsonify(task)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ==================== FILTER ENDPOINTS ====================

@app.route('/api/tasks/filter/category/<category>', methods=['GET'])
def get_tasks_by_category(category):
    """Get tasks by category"""
    tasks = load_tasks()
    filtered = [t for t in tasks if t['category'] == category]
    return jsonify(filtered)


@app.route('/api/tasks/filter/pending', methods=['GET'])
def get_pending_tasks():
    """Get all pending (incomplete) tasks"""
    tasks = load_tasks()
    pending = [t for t in tasks if not t['completed']]
    return jsonify(pending)


@app.route('/api/tasks/filter/completed', methods=['GET'])
def get_completed_tasks():
    """Get all completed tasks"""
    tasks = load_tasks()
    completed = [t for t in tasks if t['completed']]
    return jsonify(completed)


@app.route('/api/tasks/filter/overdue', methods=['GET'])
def get_overdue_tasks():
    """Get overdue tasks"""
    tasks = load_tasks()
    overdue = []
    
    for task in tasks:
        if not task['completed'] and task['deadline']:
            try:
                deadline = datetime.fromisoformat(task['deadline'].split('T')[0])
                if deadline < datetime.now().date():
                    overdue.append(task)
            except:
                pass
    
    return jsonify(overdue)


# ==================== STATISTICS ENDPOINTS ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    tasks = load_tasks()
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t['completed'])
    pending = total - completed
    
    by_category = {}
    for cat in ["Studies", "Messages", "Gym", "Food", "Other"]:
        count = sum(1 for t in tasks if t['category'] == cat and not t['completed'])
        if count > 0:
            by_category[cat] = count
    
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round(completion_rate, 1),
        "by_category": by_category
    })


@app.route('/api/stats/detailed', methods=['GET'])
def get_detailed_stats():
    """Get detailed statistics"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            stats = json.load(f)
            return jsonify(stats)
    
    return jsonify({
        "total_tasks_created": 0,
        "total_tasks_completed": 0,
        "total_check_ins": 0,
        "total_reminders": 0
    })


# ==================== SYNC ENDPOINTS ====================

@app.route('/api/sync', methods=['POST'])
def sync_data():
    """Sync data from mobile app"""
    try:
        data = request.json
        
        if 'tasks' in data:
            save_tasks(data['tasks'])
        
        return jsonify({
            "status": "synced",
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ==================== USER ENDPOINTS ====================

@app.route('/api/user', methods=['GET'])
def get_user_info():
    """Get user information"""
    config = load_config()
    return jsonify({
        "name": config.get("creator", "User"),
        "version": API_VERSION,
        "preferences": config.get("preferences", {})
    })


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """404 handler"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """500 handler"""
    return jsonify({"error": "Server error", "details": str(error)}), 500


# ==================== STARTUP ====================

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Emma AI API Server")
    print("=" * 50)
    print(f"Version: {API_VERSION}")
    print("Starting server on http://0.0.0.0:5000")
    print("=" * 50)
    print("\n📱 Mobile App can connect at: http://<your-ip>:5000")
    print("🔍 API Health Check: http://<your-ip>:5000/api/health")
    print("\nTo test locally:")
    print("  - Tasks: http://localhost:5000/api/tasks")
    print("  - Stats: http://localhost:5000/api/stats")
    print("  - Health: http://localhost:5000/api/health\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
