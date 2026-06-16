from flask import render_template, jsonify
from controllers.dashboard_controller import DashboardController

def dashboard_routes(app):
    dashboard_controller = DashboardController()
    
    @app.route('/')
    @app.route('/dashboard')
    def live_dashboard():
        """Main dashboard page"""
        data = dashboard_controller.get_dashboard_data()
        return render_template('dashboard/live_dashboard.html', data=data)
    
    @app.route('/api/realtime_data')
    def realtime_data():
        """API endpoint for real-time updates"""
        data = dashboard_controller.get_realtime_data()
        
        # Convert SQLite Row objects to dictionaries
        if 'inside_members' in data and data['inside_members']:
            members_list = []
            for member in data['inside_members']:
                if isinstance(member, (list, tuple)):
                    members_list.append({
                        'id': member[0] if len(member) > 0 else None,
                        'name': member[1] if len(member) > 1 else None,
                        'phone': member[2] if len(member) > 2 else None,
                        'trainer_name': member[3] if len(member) > 3 else None,
                        'checkin_time': member[4] if len(member) > 4 else None,
                    })
                elif hasattr(member, 'keys'):
                    members_list.append(dict(member))
                else:
                    members_list.append(member)
            data['inside_members'] = members_list
        
        return jsonify(data)
    
    @app.route('/dashboard/current_members')
    def current_members_list():
        """Partial view for current members list"""
        data = dashboard_controller.get_realtime_data()
        members = data.get('inside_members', [])
        return render_template('dashboard/current_members_list.html', members=members)
    
    @app.route('/dashboard/slot_status')
    def slot_status():
        """Partial view for slot status"""
        data = dashboard_controller.get_dashboard_data()
        slots = data.get('slot_status', [])
        return render_template('dashboard/slot_status.html', slots=slots)