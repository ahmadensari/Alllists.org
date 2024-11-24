from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes.auth import auth_routes
from routes.list import list_routes
from routes.payment import payment_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Register routes
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(list_routes, url_prefix='/lists')
app.register_blueprint(payment_routes, url_prefix='/payments')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
