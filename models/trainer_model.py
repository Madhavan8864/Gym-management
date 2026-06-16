import sqlite3
from config.db import get_db_connection

class TrainerModel:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create trainers table if not exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trainers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                speciality TEXT,
                phone TEXT,
                available_slots TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_all_trainers(self):
        """Get all trainers"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM trainers ORDER BY name')
        trainers = cursor.fetchall()
        
        conn.close()
        return trainers
    
    def get_trainer_by_id(self, trainer_id):
        """Get single trainer by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM trainers WHERE id = ?', (trainer_id,))
        trainer = cursor.fetchone()
        
        conn.close()
        return trainer
    
    def add_trainer(self, name, speciality, phone, available_slots):
        """Add new trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trainers (name, speciality, phone, available_slots)
            VALUES (?, ?, ?, ?)
        ''', (name, speciality, phone, available_slots))
        
        conn.commit()
        trainer_id = cursor.lastrowid
        conn.close()
        
        return trainer_id
    
    def update_trainer(self, trainer_id, name, speciality, phone, available_slots):
        """Update trainer details"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE trainers 
            SET name=?, speciality=?, phone=?, available_slots=?
            WHERE id=?
        ''', (name, speciality, phone, available_slots, trainer_id))
        
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        
        return updated
    
    def delete_trainer(self, trainer_id):
        """Delete trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM trainers WHERE id = ?', (trainer_id,))
        
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    def get_trainer_members_count(self, trainer_id):
        """Get count of members assigned to trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM members WHERE trainer_id = ?', (trainer_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_trainer_schedule(self, trainer_id):
        """Get trainer's schedule (members assigned)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.name, m.phone, s.slot_name, s.start_time, s.end_time
            FROM members m
            JOIN slots s ON m.slot_id = s.id
            WHERE m.trainer_id = ?
        ''', (trainer_id,))
        
        schedule = cursor.fetchall()
        conn.close()
        return schedule