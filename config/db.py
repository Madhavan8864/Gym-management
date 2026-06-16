import sqlite3
import os

DB_PATH = 'database/gym_management.db'

def get_db_connection():
    """Create and return database connection"""
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize all database tables"""
    from models.member_model import MemberModel
    from models.trainer_model import TrainerModel
    from models.attendance_model import AttendanceModel
    from models.slot_model import SlotModel
    from models.payment_model import PaymentModel
    
    # Create all tables
    MemberModel()
    TrainerModel()
    AttendanceModel()
    SlotModel()
    PaymentModel()