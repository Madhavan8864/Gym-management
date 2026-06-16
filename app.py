from flask import Flask
from routes.member_routes import member_routes
from routes.trainer_routes import trainer_routes
from routes.attendance_routes import attendance_routes
from routes.slot_routes import slot_routes
from routes.payment_routes import payment_routes
from routes.dashboard_routes import dashboard_routes
from routes.report_routes import report_routes
from routes.api_routes import api_routes
from routes.settings_routes import settings_routes  # Add this

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'

# Register all routes
member_routes(app)
trainer_routes(app)
attendance_routes(app)
slot_routes(app)
payment_routes(app)
dashboard_routes(app)
report_routes(app)
api_routes(app)
settings_routes(app)  # Add this

if __name__ == '__main__':
    app.run(debug=True)