import sqlite3
from config.db import get_db_connection

class PaymentModel:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create payments table if not exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER,
                amount REAL,
                payment_date TEXT,
                due_date TEXT,
                payment_method TEXT,
                status TEXT DEFAULT 'paid',
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_all_payments(self):
        """Get all payments with member names"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, m.name as member_name 
            FROM payments p
            JOIN members m ON p.member_id = m.id
            ORDER BY p.payment_date DESC
        ''')
        
        payments = cursor.fetchall()
        conn.close()
        return payments
    
    def add_payment(self, member_id, amount, payment_date, due_date, payment_method, status):
        """Add new payment record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO payments (member_id, amount, payment_date, due_date, payment_method, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (member_id, amount, payment_date, due_date, payment_method, status))
        
        conn.commit()
        payment_id = cursor.lastrowid
        conn.close()
        
        return payment_id
    
    def get_member_payments(self, member_id):
        """Get payment history for a member"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM payments 
            WHERE member_id = ?
            ORDER BY payment_date DESC
        ''', (member_id,))
        
        payments = cursor.fetchall()
        conn.close()
        return payments
    
    def get_pending_payments(self, current_date):
        """Get all pending payments (due date passed)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, m.name as member_name, m.phone
            FROM payments p
            JOIN members m ON p.member_id = m.id
            WHERE p.due_date < ? AND p.status = 'paid'
            ORDER BY p.due_date ASC
        ''', (current_date,))
        
        pending = cursor.fetchall()
        conn.close()
        return pending
    
    def get_monthly_collection(self, month, year):
        """Get payments for specific month"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Format month to 2 digits
        month_str = f"{month:02d}"
        
        cursor.execute('''
            SELECT p.*, m.name as member_name 
            FROM payments p
            JOIN members m ON p.member_id = m.id
            WHERE strftime('%m', payment_date) = ? AND strftime('%Y', payment_date) = ?
            ORDER BY p.payment_date DESC
        ''', (month_str, str(year)))
        
        payments = cursor.fetchall()
        conn.close()
        return payments
    
    def get_total_collection(self):
        """Get total collection amount"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(amount) FROM payments')
        total = cursor.fetchone()[0]
        
        conn.close()
        return total if total else 0