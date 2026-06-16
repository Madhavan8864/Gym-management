from models.trainer_model import TrainerModel
from utils.validation_helper import validate_phone

class TrainerController:
    def __init__(self):
        self.trainer_model = TrainerModel()
    
    def get_all_trainers(self):
        """Get all trainers list"""
        return self.trainer_model.get_all_trainers()
    
    def get_trainer_by_id(self, trainer_id):
        """Get single trainer details"""
        return self.trainer_model.get_trainer_by_id(trainer_id)
    
    def add_trainer(self, name, speciality, phone, available_slots):
        """Add new trainer"""
        if not name or len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        if not speciality:
            return False, "Please enter speciality"
        
        if not validate_phone(phone):
            return False, "Invalid phone number"
        
        result = self.trainer_model.add_trainer(name, speciality, phone, available_slots)
        
        if result:
            return True, "Trainer added successfully"
        else:
            return False, "Failed to add trainer"
    
    def update_trainer(self, trainer_id, name, speciality, phone, available_slots):
        """Update trainer details"""
        result = self.trainer_model.update_trainer(
            trainer_id, name, speciality, phone, available_slots
        )
        
        if result:
            return True, "Trainer updated successfully"
        else:
            return False, "Failed to update trainer"
    
    def delete_trainer(self, trainer_id):
        """Delete trainer"""
        # Check if trainer has members assigned
        members_count = self.trainer_model.get_trainer_members_count(trainer_id)
        
        if members_count > 0:
            return False, f"Cannot delete trainer with {members_count} assigned members"
        
        result = self.trainer_model.delete_trainer(trainer_id)
        
        if result:
            return True, "Trainer deleted successfully"
        else:
            return False, "Failed to delete trainer"
    
    def get_trainer_schedule(self, trainer_id):
        """Get trainer's schedule"""
        return self.trainer_model.get_trainer_schedule(trainer_id)