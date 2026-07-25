import sys
import io
from datetime import datetime
from brain.emma import Emma
from skills.task_manager import TaskManager
from skills.scheduler import Scheduler
from memory.memory import Memory
from logs.logger import Logger

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    emma = Emma(name="Emma", creator="Parzival", version="2.1")
    emma.boot()
    
    # Initialize all components
    task_manager = TaskManager()
    scheduler = Scheduler()
    memory = Memory()
    logger = Logger()
    
    # Log startup
    logger.log_activity("startup", "Emma started successfully")
    
    # Log interaction
    memory.log_interaction()
    
    # Try facial recognition login
    try:
        from brain.facial_recognition import FacialRecognition
        facial_system = FacialRecognition()
        
        registered_users = facial_system.get_registered_users()
        if registered_users:
            recognized_user = facial_system.recognize_faces(timeout=10)
            if recognized_user:
                emma.creator = recognized_user
                print(f"\n✅ Welcome back, {recognized_user}! 🎉\n")
    except ImportError:
        print("\n⚠️  Facial recognition not available (install: pip install opencv-python face-recognition)\n")
    except Exception as e:
        print(f"\n⚠️  Facial recognition error: {str(e)}\n")
    
    # Start interactive mode with all components
    emma.start_interactive_mode(task_manager, scheduler, memory, logger)


if __name__ == "__main__":
    main()