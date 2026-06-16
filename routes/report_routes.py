from flask import render_template, request
from controllers.report_controller import ReportController
from utils.datetime_helper import get_current_month, get_current_year

def report_routes(app):
    report_controller = ReportController()
    
    @app.route('/reports/daily')
    def daily_report():
        """Daily attendance report"""
        date = request.args.get('date')
        report = report_controller.get_daily_report(date)
        return render_template('reports/daily_report.html', report=report)
    
    # MISSING ROUTE 1: Weekly Report
    @app.route('/reports/weekly')
    def weekly_report():
        """Weekly report page"""
        return render_template('reports/weekly_report.html')
    
    # MISSING ROUTE 2: Monthly Report
    @app.route('/reports/monthly')
    def monthly_report():
        """Monthly report page"""
        return render_template('reports/monthly_report.html')
    
    @app.route('/reports/trainer')
    def trainer_report():
        """Trainer performance report"""
        report = report_controller.get_trainer_report()
        return render_template('reports/trainer_report.html', report=report)
    
    @app.route('/reports/slot')
    def slot_report():
        """Slot occupancy report"""
        report = report_controller.get_slot_occupancy_report()
        return render_template('reports/slot_occupancy_report.html', report=report)
    
    # MISSING ROUTE 3: Peak Hours Report
    @app.route('/reports/peak-hours')
    def peak_hours_report():
        """Peak hours analysis page"""
        return render_template('reports/peak_hours_report.html')
    
    @app.route('/reports/active-members')
    def active_members():
        """Active members report"""
        report = report_controller.get_members_status_report()
        return render_template('reports/active_members.html', report=report)
    
    # MISSING ROUTE 4: Inactive Members Report
    @app.route('/reports/inactive-members')
    def inactive_members():
        """Inactive members report"""
        report = report_controller.get_members_status_report()
        return render_template('reports/inactive_members.html', report=report)
    
    @app.route('/reports/revenue')
    def revenue_report():
        """Revenue report"""
        month = request.args.get('month', get_current_month())
        year = request.args.get('year', get_current_year())
        
        report = report_controller.get_revenue_report(int(month), int(year))
        return render_template('reports/revenue_report.html', report=report)