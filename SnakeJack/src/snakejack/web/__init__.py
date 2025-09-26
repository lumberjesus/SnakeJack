"""Web application module for SnakeJack."""
from flask import Flask
from flask_session import Session

app = Flask(__name__, 
           template_folder="templates",
           static_folder="static")

# Configure Flask-Session for server-side session storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "snakejack-secret"  # Change this in production
Session(app)

# Import routes after app is created to avoid circular imports
from . import routes  # noqa