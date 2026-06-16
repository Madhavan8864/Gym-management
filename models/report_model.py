import sqlite3
from config.db import get_db_connection

class ReportModel:
    def __init__(self):
        pass
    
    def get_daily_summary(self, date):
        """Get daily summary statistics"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total check-ins
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE attendance_date = ?', (date,))
        total_checkins = cursor.fetchone()[0]
        
        # Unique members
        cursor.execute('SELECT COUNT(DISTINCT member_id) FROM attendance WHERE attendance_date = ?', (date,))
        unique_members = cursor.fetchone()[0]
        
        # Average duration
        cursor.execute('SELECT AVG(duration) FROM attendance WHERE attendance_date = ? AND duration IS NOT NULL', (date,))
        avg_duration = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_checkins': total_checkins,
            'unique_members': unique_members,
            'avg_duration': round(avg_duration, 2) if avg_duration else 0
        }
    
    def get_weekly_report(self, start_date, end_date):
        """Get weekly report"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT attendance_date, COUNT(*) as count
            FROM attendance
            WHERE attendance_date BETWEEN ? AND ?
            GROUP BY attendance_date
            ORDER BY attendance_date
        ''', (start_date, end_date))
        
        report = cursor.fetchall()
        conn.close()
        return report
    
    def get_peak_hours(self):
        """Get peak hours analysis"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strftime('%H', checkin_time) as hour,
                COUNT(*) as checkin_count
            FROM attendance
            GROUP BY hour
            ORDER BY checkin_count DESC
            LIMIT 5
        ''')
        
        peak_hours = cursor.fetchall()
        conn.close()
        return peak_hours