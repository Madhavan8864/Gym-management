from models.payment_model import PaymentModel
from models.member_model import MemberModel
from utils.datetime_helper import get_current_date

class PaymentController:
    def __init__(self):
        self.payment_model = PaymentModel()
        self.member_model = MemberModel()
    
    def get_all_payments(self):
        """Get all payments"""
        return self.payment_model.get_all_payments()
    
    def add_payment(self, member_id, amount, payment_date, due_date, payment_method):
        """Add new payment record"""
        # Check if member exists
        member = self.member_model.get_member_by_id(member_id)
        
        if not member:
            return False, "Member not found"
        
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        if not payment_date:
            payment_date = get_current_date()
        
        result = self.payment_model.add_payment(
            member_id, amount, payment_date, due_date, payment_method, 'paid'
        )
        
        if result:
            return True, "Payment recorded successfully"
        else:
            return False, "Failed to record payment"
    
    def get_member_payments(self, member_id):
        """Get payment history for a member"""
        return self.payment_model.get_member_payments(member_id)
    
    def get_pending_payments(self):
        """Get all pending payments"""
        current_date = get_current_date()
        return self.payment_model.get_pending_payments(current_date)
    
    def get_monthly_collection(self, month, year):
        """Get payment collection for specific month"""
        return self.payment_model.get_monthly_collection(month, year)
    
    def get_total_collection(self):
        """Get total collection amount"""
        return self.payment_model.get_total_collection()
    
    def get_member_balance(self, member_id):
        """Calculate member's pending balance"""
        payments = self.get_member_payments(member_id)
        member = self.member_model.get_member_by_id(member_id)
        
        if not member:
            return 0
        
        total_paid = sum(p[2] for p in payments)  # amount column
        
        # Assuming monthly fee is stored in member record
        monthly_fee = member[7] if member[7] else 0  # fee_amount column
        
        # Simple calculation - can be enhanced
        balance = monthly_fee - total_paid
        
        return max(0, balance)