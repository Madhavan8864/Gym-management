from models.member_model import MemberModel
from utils.validation_helper import validate_email, validate_phone
from utils.datetime_helper import get_current_date

class MemberController:
    def __init__(self):
        self.member_model = MemberModel()
    
    def get_all_members(self):
        """Get all members list"""
        return self.member_model.get_all_members()
    
    def get_member_by_id(self, member_id):
        """Get single member details"""
        return self.member_model.get_member_by_id(member_id)
    
    def add_member(self, name, phone, email, trainer_id, slot_id, fee_amount):
        """Add new member with validation"""
        # Validation
        if not name or len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        if not validate_phone(phone):
            return False, "Invalid phone number"
        
        if email and not validate_email(email):
            return False, "Invalid email address"
        
        if not trainer_id:
            return False, "Please select a trainer"
        
        if not slot_id:
            return False, "Please select a time slot"
        
        # Add to database
        join_date = get_current_date()
        status = "active"
        
        result = self.member_model.add_member(
            name, phone, email, trainer_id, slot_id, 
            join_date, fee_amount, status
        )
        
        if result:
            return True, "Member added successfully"
        else:
            return False, "Failed to add member"
    
    def update_member(self, member_id, name, phone, email, trainer_id, slot_id, status):
        """Update existing member"""
        result = self.member_model.update_member(
            member_id, name, phone, email, trainer_id, slot_id, status
        )
        
        if result:
            return True, "Member updated successfully"
        else:
            return False, "Failed to update member"
    
    def delete_member(self, member_id):
        """Delete member"""
        result = self.member_model.delete_member(member_id)
        
        if result:
            return True, "Member deleted successfully"
        else:
            return False, "Failed to delete member"
    
    def search_members(self, search_term):
        """Search members by name or phone"""
        return self.member_model.search_members(search_term)
    
    def get_members_by_trainer(self, trainer_id):
        """Get members assigned to specific trainer"""
        return self.member_model.get_members_by_trainer(trainer_id)
    
    def get_members_by_slot(self, slot_id):
        """Get members in specific time slot"""
        return self.member_model.get_members_by_slot(slot_id)
    
    def get_active_members_count(self):
        """Get count of active members"""
        return self.member_model.get_active_members_count()