from models.attendance_model import AttendanceModel
from models.member_model import MemberModel
from utils.datetime_helper import get_current_datetime, get_current_date, get_current_time

class AttendanceController:
    def __init__(self):
        self.attendance_model = AttendanceModel()
        self.member_model = MemberModel()
    
    def member_checkin(self, member_id):
        """Mark member check-in"""
        try:
            # Check if member exists
            member = self.member_model.get_member_by_id(member_id)
            
            if not member:
                return False, "Member not found"
            
            # Check if already checked in
            if self.attendance_model.is_already_checked_in(member_id):
                return False, "Member already checked in today! Please checkout first."
            
            # Check if member is active
            member_status = member[8] if len(member) > 8 else 'inactive'
            if member_status != 'active':
                return False, "Member is not active"
            
            # Get current time
            current_datetime = get_current_datetime()
            current_date = get_current_date()
            checkin_time = get_current_time()
            
            # Add check-in record
            result = self.attendance_model.add_checkin(
                member_id, current_date, checkin_time, current_datetime
            )
            
            if result:
                return True, f"✅ Check-in successful at {checkin_time}"
            else:
                return False, "Failed to check-in"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def member_checkout(self, member_id):
        """Mark member check-out"""
        try:
            # Get current check-in record
            current_session = self.attendance_model.get_current_session(member_id)
            
            if not current_session:
                return False, "Member is not checked in! Please check-in first."
            
            # Get session ID - handle both tuple and Row object
            if isinstance(current_session, dict) or hasattr(current_session, 'keys'):
                session_id = current_session['id']
                checkin_time = current_session['checkin_time']
            else:
                session_id = current_session[0]
                checkin_time = current_session[3]
            
            checkout_time = get_current_time()
            
            # Calculate duration
            duration = self.calculate_duration(checkin_time, checkout_time)
            
            # Update check-out
            result = self.attendance_model.update_checkout(session_id, checkout_time, duration)
            
            if result:
                return True, f"✅ Check-out successful! Duration: {duration} minutes"
            else:
                return False, "Failed to check-out"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def calculate_duration(self, checkin_time, checkout_time):
        """Calculate duration in minutes"""
        from datetime import datetime
        
        try:
            # Convert string times to datetime objects
            checkin = datetime.strptime(str(checkin_time), '%H:%M:%S')
            checkout = datetime.strptime(str(checkout_time), '%H:%M:%S')
            
            # Calculate difference
            duration = (checkout - checkin).seconds // 60
            
            # Handle case when checkout is next day
            if duration < 0:
                duration = 0
                
            return duration
        except Exception as e:
            print(f"Duration calculation error: {e}")
            return 0
    
    def get_current_inside_members(self):
        """Get list of members currently inside gym"""
        try:
            return self.attendance_model.get_current_inside_members()
        except Exception as e:
            print(f"Error getting inside members: {e}")
            return []
    
    def get_today_attendance(self):
        """Get today's all attendance records"""
        try:
            current_date = get_current_date()
            return self.attendance_model.get_attendance_by_date(current_date)
        except Exception as e:
            print(f"Error getting today attendance: {e}")
            return []
    
    def get_attendance_by_date(self, date=None):
        """Get attendance records for a specific date"""
        from utils.datetime_helper import get_current_date
        
        try:
            if not date:
                date = get_current_date()
            return self.attendance_model.get_attendance_by_date(date)
        except Exception as e:
            print(f"Error getting attendance by date: {e}")
            return []
    
    def get_member_attendance_history(self, member_id):
        """Get attendance history for a member"""
        try:
            return self.attendance_model.get_member_attendance(member_id)
        except Exception as e:
            print(f"Error getting member attendance: {e}")
            return []
    
    def get_today_checkin_count(self):
        """Get today's total check-in count"""
        try:
            current_date = get_current_date()
            return self.attendance_model.get_checkin_count_by_date(current_date)
        except Exception as e:
            print(f"Error getting check-in count: {e}")
            return 0
    
    def get_current_inside_count(self):
        """Get count of members currently inside"""
        try:
            members = self.get_current_inside_members()
            return len(members) if members else 0
        except Exception as e:
            print(f"Error getting inside count: {e}")
            return 0