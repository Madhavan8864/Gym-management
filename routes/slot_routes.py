from flask import render_template, request, redirect, url_for, flash
from controllers.slot_controller import SlotController
from controllers.member_controller import MemberController

def slot_routes(app):
    slot_controller = SlotController()
    member_controller = MemberController()
    
    @app.route('/slots')
    def view_slots():
        """View all time slots"""
        slots = slot_controller.get_all_slots()
        return render_template('slots/view_slots.html', slots=slots)
    
    @app.route('/slots/add', methods=['GET', 'POST'])
    def add_slot():
        """Add new time slot"""
        if request.method == 'POST':
            slot_name = request.form.get('slot_name')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            max_capacity = request.form.get('max_capacity', 20)
            
            success, message = slot_controller.add_slot(
                slot_name, start_time, end_time, int(max_capacity)
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_slots'))
        
        return render_template('slots/add_slot.html')
    
    @app.route('/slots/edit/<int:slot_id>', methods=['GET', 'POST'])
    def edit_slot(slot_id):
        """Edit time slot"""
        if request.method == 'POST':
            slot_name = request.form.get('slot_name')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            max_capacity = request.form.get('max_capacity')
            
            success, message = slot_controller.update_slot(
                slot_id, slot_name, start_time, end_time, int(max_capacity)
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_slots'))
        
        slot = slot_controller.get_slot_by_id(slot_id)
        return render_template('slots/edit_slot.html', slot=slot)
    
    @app.route('/slots/delete/<int:slot_id>')
    def delete_slot(slot_id):
        """Delete time slot"""
        success, message = slot_controller.delete_slot(slot_id)
        flash(message)
        return redirect(url_for('view_slots'))
    
    @app.route('/slots/capacity')
    def slot_capacity():
        """View slot capacity status"""
        status = slot_controller.get_all_slots_status()
        return render_template('slots/slot_capacity.html', status=status)
    
    # MISSING ROUTE 1: Manage Slots
    @app.route('/slots/manage')
    def manage_slots():
        """Manage all slots page"""
        slots = slot_controller.get_all_slots()
        return render_template('slots/manage_slots.html', slots=slots)
    
    # MISSING ROUTE 2: Assign Member to Slot
    @app.route('/slots/assign/<int:member_id>', methods=['GET', 'POST'])
    def assign_member_slot(member_id):
        """Assign member to a time slot"""
        if request.method == 'POST':
            slot_id = request.form.get('slot_id')
            member = member_controller.get_member_by_id(member_id)
            if member:
                success, message = member_controller.update_member(
                    member_id, member[1], member[2], member[3], 
                    member[4], slot_id, member[8]
                )
                flash(message)
            return redirect(url_for('member_details', member_id=member_id))
        
        member = member_controller.get_member_by_id(member_id)
        slots = slot_controller.get_all_slots()
        return render_template('slots/assign_member_slot.html', member=member, slots=slots)