from flask import Blueprint

# Create a blueprint instead of importing the app
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "<h1>Ward 42 Fix-It is running!</h1><p>We will build the real home page soon.</p>"