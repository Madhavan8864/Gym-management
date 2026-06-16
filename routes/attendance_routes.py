from flask import render_template, request, redirect, url_for, flash, jsonify
from controllers.attendance_controller import AttendanceController
from controllers.member_controller import MemberController

def attendance_routes(app):
    attendance_controller = AttendanceController()
    member_controller = MemberController()
    
    @app.route('/attendance/checkin', methods=['GET', 'POST'])
    def checkin():
        """Member check-in page"""
        if request.method == 'POST':
            member_id = request.form.get('member_id')
            success, message = attendance_controller.member_checkin(member_id)
            flash(message)
            
            if success:
                return redirect(url_for('live_dashboard'))
        
        members = member_controller.get_all_members()
        return render_template('attendance/checkin.html', members=members)
    
    @app.route('/attendance/checkout', methods=['GET', 'POST'])
    def checkout():
        """Member check-out page"""
        if request.method == 'POST':
            member_id = request.form.get('member_id')
            success, message = attendance_controller.member_checkout(member_id)
            flash(message)
            
            if success:
                return redirect(url_for('live_dashboard'))
        
        inside_members = attendance_controller.get_current_inside_members()
        return render_template('attendance/checkout.html', members=inside_members)
    
    @app.route('/attendance/quick')
    def quick_checkin():
        """Quick check-in page with search"""
        return render_template('attendance/quick_checkin.html')
    
    @app.route('/attendance/today')
    def today_attendance():
        """Today's attendance report"""
        attendance = attendance_controller.get_today_attendance()
        return render_template('attendance/today_attendance.html', attendance=attendance)
    
    @app.route('/attendance/member/<int:member_id>')
    def member_attendance(member_id):
        """Member attendance history"""
        history = attendance_controller.get_member_attendance_history(member_id)
        member = member_controller.get_member_by_id(member_id)
        return render_template('attendance/member_attendance.html', 
                             member=member, history=history)
    
    @app.route('/attendance/current')
    def current_inside():
        """Current inside members"""
        members = attendance_controller.get_current_inside_members()
        return render_template('attendance/current_inside_members.html', members=members)