from utils.datetime_helper import get_current_time

class RealtimeTracker:
    """Helper class for real-time tracking"""
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in minutes/seconds"""
        if not seconds:
            return "Just now"
        
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} min{'s' if minutes > 1 else ''}"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m"
    
    @staticmethod
    def calculate_session_duration(checkin_time):
        """Calculate how long member has been inside"""
        from datetime import datetime
        current = datetime.now()
        checkin = datetime.strptime(checkin_time, '%H:%M:%S')
        
        # Replace date with today
        checkin = checkin.replace(year=current.year, month=current.month, day=current.day)
        
        duration = (current - checkin).seconds
        return duration
    
    @staticmethod
    def get_slot_by_current_time():
        """Get current time slot based on time"""
        current_time = get_current_time()
        
        # Define time slots
        slots = {
            'Morning': ('06:00:00', '08:00:00'),
            'Late Morning': ('08:00:00', '10:00:00'),
            'Afternoon': ('16:00:00', '18:00:00'),
            'Evening': ('18:00:00', '20:00:00'),
            'Night': ('20:00:00', '22:00:00')
        }
        
        for slot_name, (start, end) in slots.items():
            if start <= current_time <= end:
                return slot_name
        
        return 'Off Hours'