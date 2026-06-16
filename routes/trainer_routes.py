from flask import render_template, request, redirect, url_for, flash
from controllers.trainer_controller import TrainerController
from controllers.member_controller import MemberController
from controllers.slot_controller import SlotController

def trainer_routes(app):
    trainer_controller = TrainerController()
    member_controller = MemberController()
    slot_controller = SlotController()
    
    @app.route('/trainers')
    def view_trainers():
        """View all trainers"""
        trainers = trainer_controller.get_all_trainers()
        return render_template('trainers/view_trainers.html', trainers=trainers)
    
    @app.route('/trainers/add', methods=['GET', 'POST'])
    def add_trainer():
        """Add new trainer"""
        if request.method == 'POST':
            name = request.form.get('name')
            speciality = request.form.get('speciality')
            phone = request.form.get('phone')
            available_slots = request.form.get('available_slots')
            
            success, message = trainer_controller.add_trainer(
                name, speciality, phone, available_slots
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_trainers'))
        
        return render_template('trainers/add_trainer.html')
    
    @app.route('/trainers/edit/<int:trainer_id>', methods=['GET', 'POST'])
    def edit_trainer(trainer_id):
        """Edit trainer"""
        if request.method == 'POST':
            name = request.form.get('name')
            speciality = request.form.get('speciality')
            phone = request.form.get('phone')
            available_slots = request.form.get('available_slots')
            
            success, message = trainer_controller.update_trainer(
                trainer_id, name, speciality, phone, available_slots
            )
            
            flash(message)
            
            if success:
                return redirect(url_for('view_trainers'))
        
        trainer = trainer_controller.get_trainer_by_id(trainer_id)
        return render_template('trainers/edit_trainer.html', trainer=trainer)
    
    @app.route('/trainers/delete/<int:trainer_id>')
    def delete_trainer(trainer_id):
        """Delete trainer"""
        success, message = trainer_controller.delete_trainer(trainer_id)
        flash(message)
        return redirect(url_for('view_trainers'))
    
    @app.route('/trainers/view/<int:trainer_id>')
    def trainer_details(trainer_id):
        """View trainer details"""
        trainer = trainer_controller.get_trainer_by_id(trainer_id)
        schedule = trainer_controller.get_trainer_schedule(trainer_id)
        return render_template('trainers/trainer_details.html', 
                             trainer=trainer, schedule=schedule)
    
    @app.route('/trainers/schedule/<int:trainer_id>')
    def trainer_schedule(trainer_id):
        """View trainer schedule with members"""
        trainer = trainer_controller.get_trainer_by_id(trainer_id)
        members = member_controller.get_members_by_trainer(trainer_id)
        
        # Organize by slot
        schedule = {}
        all_slots = slot_controller.get_all_slots()
        
        for slot in all_slots:
            slot_name = slot[1]
            schedule[slot_name] = []
        
        for member in members:
            slot_id = member[5]
            for slot in all_slots:
                if slot[0] == slot_id:
                    schedule[slot[1]].append({
                        'name': member[1],
                        'join_date': member[6],
                        'status': member[8]
                    })
                    break
        
        return render_template('trainers/trainer_schedule.html', 
                             trainer=trainer, schedule=schedule)