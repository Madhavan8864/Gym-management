import sqlite3
from config.db import get_db_connection

class SlotModel:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create slots table if not exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_name TEXT NOT NULL,
                start_time TEXT,
                end_time TEXT,
                max_capacity INTEGER DEFAULT 20
            )
        ''')
        
        # Insert default slots if table is empty
        cursor.execute('SELECT COUNT(*) FROM slots')
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_slots = [
                ('Morning', '06:00:00', '08:00:00', 20),
                ('Late Morning', '08:00:00', '10:00:00', 20),
                ('Afternoon', '16:00:00', '18:00:00', 20),
                ('Evening', '18:00:00', '20:00:00', 20),
                ('Night', '20:00:00', '22:00:00', 20)
            ]
            cursor.executemany('''
                INSERT INTO slots (slot_name, start_time, end_time, max_capacity)
                VALUES (?, ?, ?, ?)
            ''', default_slots)
        
        conn.commit()
        conn.close()
    
    def get_all_slots(self):
        """Get all time slots"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM slots ORDER BY start_time')
        slots = cursor.fetchall()
        
        conn.close()
        return slots
    
    def get_slot_by_id(self, slot_id):
        """Get single slot by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM slots WHERE id = ?', (slot_id,))
        slot = cursor.fetchone()
        
        conn.close()
        return slot
    
    def add_slot(self, slot_name, start_time, end_time, max_capacity):
        """Add new time slot"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO slots (slot_name, start_time, end_time, max_capacity)
            VALUES (?, ?, ?, ?)
        ''', (slot_name, start_time, end_time, max_capacity))
        
        conn.commit()
        slot_id = cursor.lastrowid
        conn.close()
        
        return slot_id
    
    def update_slot(self, slot_id, slot_name, start_time, end_time, max_capacity):
        """Update time slot"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE slots 
            SET slot_name=?, start_time=?, end_time=?, max_capacity=?
            WHERE id=?
        ''', (slot_name, start_time, end_time, max_capacity, slot_id))
        
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        
        return updated
    
    def delete_slot(self, slot_id):
        """Delete time slot"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM slots WHERE id = ?', (slot_id,))
        
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    def get_slot_occupancy(self, slot_id):
        """Get current number of members in slot"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM members WHERE slot_id = ?', (slot_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count