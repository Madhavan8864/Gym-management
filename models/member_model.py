import sqlite3
from config.db import get_db_connection

class MemberModel:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create members table if not exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                trainer_id INTEGER,
                slot_id INTEGER,
                join_date TEXT,
                fee_amount REAL,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (trainer_id) REFERENCES trainers(id),
                FOREIGN KEY (slot_id) REFERENCES slots(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_all_members(self):
        """Get all members with trainer and slot names"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, t.name as trainer_name, s.slot_name 
            FROM members m
            LEFT JOIN trainers t ON m.trainer_id = t.id
            LEFT JOIN slots s ON m.slot_id = s.id
            ORDER BY m.id DESC
        ''')
        
        members = cursor.fetchall()
        conn.close()
        return members
    
    def get_member_by_id(self, member_id):
        """Get single member by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM members WHERE id = ?', (member_id,))
        member = cursor.fetchone()
        
        conn.close()
        return member
    
    def add_member(self, name, phone, email, trainer_id, slot_id, join_date, fee_amount, status):
        """Add new member"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO members (name, phone, email, trainer_id, slot_id, join_date, fee_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, trainer_id, slot_id, join_date, fee_amount, status))
        
        conn.commit()
        member_id = cursor.lastrowid
        conn.close()
        
        return member_id
    
    def update_member(self, member_id, name, phone, email, trainer_id, slot_id, status):
        """Update member details"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE members 
            SET name=?, phone=?, email=?, trainer_id=?, slot_id=?, status=?
            WHERE id=?
        ''', (name, phone, email, trainer_id, slot_id, status, member_id))
        
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        
        return updated
    
    def delete_member(self, member_id):
        """Delete member"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM members WHERE id = ?', (member_id,))
        
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    def search_members(self, search_term):
        """Search members by name or phone"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM members 
            WHERE name LIKE ? OR phone LIKE ?
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        members = cursor.fetchall()
        conn.close()
        return members
    
    def get_members_by_trainer(self, trainer_id):
        """Get members assigned to a trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM members WHERE trainer_id = ?', (trainer_id,))
        members = cursor.fetchall()
        
        conn.close()
        return members
    
    def get_members_by_slot(self, slot_id):
        """Get members in a time slot"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM members WHERE slot_id = ?', (slot_id,))
        members = cursor.fetchall()
        
        conn.close()
        return members
    
    def get_members_by_slot_count(self, slot_id):
        """Get count of members in a slot"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM members WHERE slot_id = ?', (slot_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_active_members_count(self):
        """Get count of active members"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM members WHERE status = "active"')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count