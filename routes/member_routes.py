from flask import render_template, request, redirect, url_for, flash
from controllers.member_controller import MemberController
from controllers.trainer_controller import TrainerController
from controllers.slot_controller import SlotController

def member_routes(app):
    member_controller = MemberController()
    trainer_controller = TrainerController()
    slot_controller = SlotController()
    
    @app.route('/members')
    def view_members():
        """View all members"""
        members = member_controller.get_all_members()
        return render_template('members/view_members.html', members=members)
    
    @app.route('/members/add', methods=['GET', 'POST'])
    def add_member():
        """Add new member"""
        if request.method == 'POST':
            name = request.form.get('name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            trainer_id = request.form.get('trainer_id')
            slot_id = request.form.get('slot_id')
            fee_amount = request.form.get('fee_amount', 0)
            
            success, message = member_controller.add_member(
                name, phone, email, trainer_id, slot_id, fee_amount
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_members'))
        
        trainers = trainer_controller.get_all_trainers()
        slots = slot_controller.get_all_slots()
        return render_template('members/add_member.html', trainers=trainers, slots=slots)
    
    @app.route('/members/edit/<int:member_id>', methods=['GET', 'POST'])
    def edit_member(member_id):
        """Edit member"""
        if request.method == 'POST':
            name = request.form.get('name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            trainer_id = request.form.get('trainer_id')
            slot_id = request.form.get('slot_id')
            status = request.form.get('status')
            
            success, message = member_controller.update_member(
                member_id, name, phone, email, trainer_id, slot_id, status
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_members'))
        
        member = member_controller.get_member_by_id(member_id)
        trainers = trainer_controller.get_all_trainers()
        slots = slot_controller.get_all_slots()
        
        return render_template('members/edit_member.html', 
                             member=member, trainers=trainers, slots=slots)
    
    @app.route('/members/delete/<int:member_id>')
    def delete_member(member_id):
        """Delete member"""
        success, message = member_controller.delete_member(member_id)
        flash(message)
        return redirect(url_for('view_members'))
    
    @app.route('/members/view/<int:member_id>')
    def member_details(member_id):
        """View member details"""
        member = member_controller.get_member_by_id(member_id)
        return render_template('members/member_details.html', member=member)
    
    @app.route('/members/search')
    def search_members():
        """Search members"""
        search_term = request.args.get('search', '')
        members = member_controller.search_members(search_term)
        return render_template('members/view_members.html', members=members)
    
    @app.route('/members/assign/<int:member_id>', methods=['GET', 'POST'])
    def assign_trainer_slot(member_id):
        """Assign trainer and slot to member"""
        if request.method == 'POST':
            trainer_id = request.form.get('trainer_id')
            slot_id = request.form.get('slot_id')
            
            member = member_controller.get_member_by_id(member_id)
            success, message = member_controller.update_member(
                member_id, member[1], member[2], member[3], 
                trainer_id, slot_id, member[8]
            )
            
            flash(message)
            return redirect(url_for('member_details', member_id=member_id))
        
        member = member_controller.get_member_by_id(member_id)
        trainers = trainer_controller.get_all_trainers()
        slots = slot_controller.get_all_slots()
        
        # Get current trainer and slot names
        current_trainer = "Not Assigned"
        current_slot = "Not Assigned"
        
        for trainer in trainers:
            if trainer[0] == member[4]:
                current_trainer = trainer[1]
                break
        
        for slot in slots:
            if slot[0] == member[5]:
                current_slot = slot[1]
                break
        
        return render_template('members/assign_trainer_slot.html', 
                             member=member, trainers=trainers, slots=slots,
                             current_trainer=current_trainer, current_slot=current_slot)