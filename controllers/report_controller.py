from controllers.member_controller import MemberController
from controllers.trainer_controller import TrainerController  # Add this import
from controllers.attendance_controller import AttendanceController
from controllers.payment_controller import PaymentController
from controllers.slot_controller import SlotController
from utils.datetime_helper import get_current_date

class ReportController:
    def __init__(self):
        self.member_controller = MemberController()
        self.trainer_controller = TrainerController()  # Add this line
        self.attendance_controller = AttendanceController()
        self.payment_controller = PaymentController()
        self.slot_controller = SlotController()
    
    def get_daily_report(self, date=None):
        """Get daily report"""
        if not date:
            date = get_current_date()
        
        # Get attendance for the date
        attendance = self.attendance_controller.get_attendance_by_date(date)
        
        # Calculate statistics
        total_checkins = len(attendance) if attendance else 0
        
        # Get unique members count
        unique_members = 0
        if attendance:
            unique_members = len(set([a[1] if hasattr(a, '__getitem__') else a['member_id'] for a in attendance]))
        
        # Calculate average duration
        durations = []
        for a in attendance:
            if hasattr(a, '__getitem__'):
                duration = a[5] if len(a) > 5 else None
            else:
                duration = a.get('duration')
            if duration:
                durations.append(duration)
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'date': date,
            'total_checkins': total_checkins,
            'unique_members': unique_members,
            'avg_duration': round(avg_duration, 2),
            'attendance_list': attendance
        }
    
    def get_trainer_report(self):
        """Get trainer performance report"""
        trainers = self.trainer_controller.get_all_trainers()
        report_data = []
        
        for trainer in trainers:
            trainer_id = trainer[0] if hasattr(trainer, '__getitem__') else trainer['id']
            members = self.member_controller.get_members_by_trainer(trainer_id)
            
            report_data.append({
                'trainer_id': trainer_id,
                'trainer_name': trainer[1] if hasattr(trainer, '__getitem__') else trainer['name'],
                'speciality': trainer[2] if hasattr(trainer, '__getitem__') else trainer.get('speciality', ''),
                'total_members': len(members) if members else 0,
                'members_list': members if members else []
            })
        
        return report_data
    
    def get_slot_occupancy_report(self):
        """Get slot occupancy report"""
        return self.slot_controller.get_all_slots_status()
    
    def get_revenue_report(self, month, year):
        """Get revenue report"""
        collection = self.payment_controller.get_monthly_collection(month, year)
        total = 0
        if collection:
            for p in collection:
                amount = p[2] if hasattr(p, '__getitem__') else p.get('amount', 0)
                total += amount if amount else 0
        
        return {
            'month': month,
            'year': year,
            'total_revenue': total,
            'payments_list': collection if collection else []
        }
    
    def get_members_status_report(self):
        """Get active vs inactive members report"""
        all_members = self.member_controller.get_all_members()
        
        active = []
        inactive = []
        
        if all_members:
            for m in all_members:
                status = m[8] if hasattr(m, '__getitem__') else m.get('status', 'inactive')
                if status == 'active':
                    active.append(m)
                else:
                    inactive.append(m)
        
        return {
            'total': len(all_members) if all_members else 0,
            'active_count': len(active),
            'inactive_count': len(inactive),
            'active_members': active,
            'inactive_members': inactive
        }