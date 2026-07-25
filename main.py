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
    emma = Emma(name="Emma", creator="Parzival", version="2.0")
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
    
    # Start interactive mode with all components
    emma.start_interactive_mode(task_manager, scheduler, memory, logger)


if __name__ == "__main__":
    main()