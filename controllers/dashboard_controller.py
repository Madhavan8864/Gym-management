from controllers.member_controller import MemberController
from controllers.trainer_controller import TrainerController
from controllers.attendance_controller import AttendanceController
from controllers.payment_controller import PaymentController
from controllers.slot_controller import SlotController
from utils.datetime_helper import get_current_date, get_current_time

class DashboardController:
    def __init__(self):
        self.member_controller = MemberController()
        self.trainer_controller = TrainerController()
        self.attendance_controller = AttendanceController()
        self.payment_controller = PaymentController()
        self.slot_controller = SlotController()
    
    def get_dashboard_data(self):
        """Get all data for dashboard"""
        current_time = get_current_time()
        current_date = get_current_date()
        
        # Get counts
        all_members = self.member_controller.get_all_members()
        total_members = len(all_members) if all_members else 0
        active_members = self.member_controller.get_active_members_count()
        
        all_trainers = self.trainer_controller.get_all_trainers()
        total_trainers = len(all_trainers) if all_trainers else 0
        
        current_inside = self.attendance_controller.get_current_inside_count()
        today_checkins = self.attendance_controller.get_today_checkin_count()
        
        pending = self.payment_controller.get_pending_payments()
        pending_payments = len(pending) if pending else 0
        
        # Get lists
        inside_members_raw = self.attendance_controller.get_current_inside_members()
        inside_members = self._convert_to_serializable(inside_members_raw)
        
        today_attendance_raw = self.attendance_controller.get_today_attendance()
        today_attendance = self._convert_to_serializable(today_attendance_raw)
        
        slot_status = self.slot_controller.get_all_slots_status()
        
        dashboard_data = {
            'current_date': current_date,
            'current_time': current_time,
            'total_members': total_members,
            'active_members': active_members,
            'total_trainers': total_trainers,
            'current_inside': current_inside,
            'today_checkins': today_checkins,
            'pending_payments': pending_payments,
            'inside_members': inside_members,
            'today_attendance': today_attendance,
            'slot_status': slot_status
        }
        
        return dashboard_data
    
    def get_realtime_data(self):
        """Get real-time data for auto-refresh"""
        inside_members_raw = self.attendance_controller.get_current_inside_members()
        
        # Convert to serializable format
        serializable_members = self._convert_to_serializable(inside_members_raw)
        
        return {
            'current_inside': len(inside_members_raw) if inside_members_raw else 0,
            'inside_members': serializable_members,
            'current_time': get_current_time()
        }
    
    def _convert_to_serializable(self, data):
        """Convert SQLite Row objects to dictionaries"""
        if not data:
            return []
        
        result = []
        for row in data:
            if row is None:
                continue
                
            if isinstance(row, dict):
                result.append(row)
            elif hasattr(row, 'keys'):  # SQLite Row object
                result.append(dict(row))
            elif isinstance(row, (list, tuple)):
                # Convert tuple to dictionary with meaningful keys
                item = {}
                if len(row) > 0: item['id'] = row[0]
                if len(row) > 1: item['name'] = row[1]
                if len(row) > 2: item['phone'] = row[2]
                if len(row) > 3: item['trainer_name'] = row[3]
                if len(row) > 4: item['checkin_time'] = row[4]
                if len(row) > 5: item['attendance_date'] = row[5]
                if len(row) > 6: item['member_name'] = row[6]
                if len(row) > 7: item['duration'] = row[7]
                result.append(item)
            else:
                result.append(row)
        
        return result