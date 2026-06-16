import sqlite3
from config.db import get_db_connection

class AttendanceModel:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create attendance table if not exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER,
                attendance_date TEXT,
                checkin_time TEXT,
                checkout_time TEXT,
                duration INTEGER,
                session_start TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_checkin(self, member_id, attendance_date, checkin_time, session_start):
        """Add check-in record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attendance (member_id, attendance_date, checkin_time, session_start)
            VALUES (?, ?, ?, ?)
        ''', (member_id, attendance_date, checkin_time, session_start))
        
        conn.commit()
        attendance_id = cursor.lastrowid
        conn.close()
        
        return attendance_id
    
    def update_checkout(self, attendance_id, checkout_time, duration):
        """Update check-out time"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE attendance 
            SET checkout_time=?, duration=?
            WHERE id=?
        ''', (checkout_time, duration, attendance_id))
        
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        
        return updated
    
    def is_already_checked_in(self, member_id):
        """Check if member already checked in today and not checked out"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE member_id = ? AND checkout_time IS NULL
            ORDER BY id DESC LIMIT 1
        ''', (member_id,))
        
        record = cursor.fetchone()
        conn.close()
        
        return record is not None
    
    def get_current_session(self, member_id):
        """Get current active session for member"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE member_id = ? AND checkout_time IS NULL
            ORDER BY id DESC LIMIT 1
        ''', (member_id,))
        
        session = cursor.fetchone()
        conn.close()
        
        return session
    
    def get_current_inside_members(self):
        """Get all members currently inside gym"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, m.name, m.phone, t.name as trainer_name, a.checkin_time, a.attendance_date
            FROM attendance a
            JOIN members m ON a.member_id = m.id
            LEFT JOIN trainers t ON m.trainer_id = t.id
            WHERE a.checkout_time IS NULL
            ORDER BY a.checkin_time DESC
        ''')
        
        members = cursor.fetchall()
        conn.close()
        return members
    
    def get_attendance_by_date(self, date):
        """Get attendance records for specific date"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, m.name, m.phone, t.name as trainer_name
            FROM attendance a
            JOIN members m ON a.member_id = m.id
            LEFT JOIN trainers t ON m.trainer_id = t.id
            WHERE a.attendance_date = ?
            ORDER BY a.checkin_time DESC
        ''', (date,))
        
        records = cursor.fetchall()
        conn.close()
        return records
    
    def get_member_attendance(self, member_id):
        """Get attendance history for a member"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE member_id = ?
            ORDER BY attendance_date DESC, checkin_time DESC
        ''', (member_id,))
        
        history = cursor.fetchall()
        conn.close()
        return history
    
    def get_checkin_count_by_date(self, date):
        """Get total check-ins for a date"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE attendance_date = ?', (date,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count