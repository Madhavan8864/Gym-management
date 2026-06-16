from flask import jsonify, request
from controllers.attendance_controller import AttendanceController
from controllers.member_controller import MemberController
from controllers.dashboard_controller import DashboardController

def api_routes(app):
    attendance_controller = AttendanceController()
    member_controller = MemberController()
    dashboard_controller = DashboardController()
    
    @app.route('/api/members/search')
    def api_search_members():
        """API endpoint to search members"""
        search_term = request.args.get('q', '')
        members = member_controller.search_members(search_term)
        
        results = []
        for member in members:
            # Convert tuple/row to dictionary
            if member:
                results.append({
                    'id': member[0],
                    'name': member[1],
                    'phone': member[2]
                })
        
        return jsonify(results)
    
    @app.route('/api/members/checkin', methods=['POST'])
    def api_checkin():
        """API endpoint for check-in"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'message': 'Invalid request'})
            
            member_id = data.get('member_id')
            if not member_id:
                return jsonify({'success': False, 'message': 'Member ID required'})
            
            success, message = attendance_controller.member_checkin(member_id)
            return jsonify({'success': success, 'message': message})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    @app.route('/api/members/checkout', methods=['POST'])
    def api_checkout():
        """API endpoint for check-out"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'message': 'Invalid request'})
            
            member_id = data.get('member_id')
            if not member_id:
                return jsonify({'success': False, 'message': 'Member ID required'})
            
            success, message = attendance_controller.member_checkout(member_id)
            return jsonify({'success': success, 'message': message})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    @app.route('/api/dashboard/stats')
    def api_dashboard_stats():
        """API endpoint for dashboard statistics"""
        try:
            data = dashboard_controller.get_realtime_data()
            
            # Convert members to serializable format
            if 'inside_members' in data and data['inside_members']:
                members_list = []
                for member in data['inside_members']:
                    if isinstance(member, (list, tuple)):
                        members_list.append({
                            'id': member[0] if len(member) > 0 else None,
                            'name': member[1] if len(member) > 1 else None
                        })
                    elif hasattr(member, 'keys'):
                        members_list.append(dict(member))
                    else:
                        members_list.append(member)
                data['inside_members'] = members_list
            
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': str(e), 'current_inside': 0, 'inside_members': []})
    
    @app.route('/api/current_inside')
    def api_current_inside():
        """API endpoint to get current inside members"""
        try:
            members = attendance_controller.get_current_inside_members()
            results = []
            
            for member in members:
                if member:
                    results.append({
                        'id': member[0] if len(member) > 0 else None,
                        'name': member[1] if len(member) > 1 else None,
                        'checkin_time': member[4] if len(member) > 4 else None
                    })
            
            return jsonify(results)
        except Exception as e:
            return jsonify([])