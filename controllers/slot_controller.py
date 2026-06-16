from models.slot_model import SlotModel
from models.member_model import MemberModel

class SlotController:
    def __init__(self):
        self.slot_model = SlotModel()
        self.member_model = MemberModel()
    
    def get_all_slots(self):
        """Get all time slots"""
        return self.slot_model.get_all_slots()
    
    def get_slot_by_id(self, slot_id):
        """Get single slot details"""
        return self.slot_model.get_slot_by_id(slot_id)
    
    def add_slot(self, slot_name, start_time, end_time, max_capacity):
        """Add new time slot"""
        if not slot_name:
            return False, "Slot name is required"
        
        if not start_time or not end_time:
            return False, "Start time and end time are required"
        
        if max_capacity <= 0:
            return False, "Capacity must be greater than 0"
        
        result = self.slot_model.add_slot(slot_name, start_time, end_time, max_capacity)
        
        if result:
            return True, "Time slot added successfully"
        else:
            return False, "Failed to add time slot"
    
    def update_slot(self, slot_id, slot_name, start_time, end_time, max_capacity):
        """Update time slot"""
        result = self.slot_model.update_slot(
            slot_id, slot_name, start_time, end_time, max_capacity
        )
        
        if result:
            return True, "Time slot updated successfully"
        else:
            return False, "Failed to update time slot"
    
    def delete_slot(self, slot_id):
        """Delete time slot"""
        # Check if members are assigned to this slot
        members_count = self.member_model.get_members_by_slot_count(slot_id)
        
        if members_count > 0:
            return False, f"Cannot delete slot with {members_count} assigned members"
        
        result = self.slot_model.delete_slot(slot_id)
        
        if result:
            return True, "Time slot deleted successfully"
        else:
            return False, "Failed to delete time slot"
    
    def get_slot_capacity_status(self, slot_id):
        """Get current occupancy for a slot"""
        slot = self.get_slot_by_id(slot_id)
        if not slot:
            return None
        
        total_members = self.member_model.get_members_by_slot_count(slot_id)
        max_capacity = slot[4]  # max_capacity column
        
        available = max_capacity - total_members
        percentage = (total_members / max_capacity) * 100 if max_capacity > 0 else 0
        
        return {
            'total_members': total_members,
            'max_capacity': max_capacity,
            'available': available,
            'percentage': round(percentage, 2)
        }
    
    def get_all_slots_status(self):
        """Get status for all slots"""
        slots = self.get_all_slots()
        status_list = []
        
        for slot in slots:
            status = self.get_slot_capacity_status(slot[0])
            status_list.append({
                'slot_id': slot[0],
                'slot_name': slot[1],
                'start_time': slot[2],
                'end_time': slot[3],
                'status': status
            })
        
        return status_list