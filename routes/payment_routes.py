from flask import render_template, request, redirect, url_for, flash
from controllers.payment_controller import PaymentController
from controllers.member_controller import MemberController

def payment_routes(app):
    payment_controller = PaymentController()
    member_controller = MemberController()
    
    @app.route('/payments')
    def view_payments():
        """View all payments"""
        payments = payment_controller.get_all_payments()
        return render_template('payments/payment_history.html', payments=payments)
    
    @app.route('/payments/add', methods=['GET', 'POST'])
    def add_payment():
        """Add new payment"""
        if request.method == 'POST':
            member_id = request.form.get('member_id')
            amount = request.form.get('amount')
            due_date = request.form.get('due_date')
            payment_method = request.form.get('payment_method')
            
            success, message = payment_controller.add_payment(
                member_id, float(amount), None, due_date, payment_method
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_payments'))
        
        members = member_controller.get_all_members()
        return render_template('payments/add_payment.html', members=members)
    
    @app.route('/payments/pending')
    def pending_payments():
        """View pending payments"""
        pending = payment_controller.get_pending_payments()
        return render_template('payments/pending_payments.html', pending=pending)
    
    @app.route('/payments/member/<int:member_id>')
    def member_payments(member_id):
        """Member payment history"""
        payments = payment_controller.get_member_payments(member_id)
        member = member_controller.get_member_by_id(member_id)
        balance = payment_controller.get_member_balance(member_id)
        
        return render_template('payments/member_payments.html', 
                             member=member, payments=payments, balance=balance)
    
    @app.route('/payments/monthly')
    def monthly_collection():
        """Monthly collection report"""
        return render_template('payments/monthly_collection.html')