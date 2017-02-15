from flask import Flask

app = Flask(__name__)

# Configurations
app.config.from_object('config.default')

from app import views  # Import routes