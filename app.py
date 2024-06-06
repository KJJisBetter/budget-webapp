from flask import Flask, request, redirect, render_template, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from config import DevelopmentConfig, ProductionConfig
from supabase import create_client
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


# Supabase client = database connection
supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = supabase.auth.get_user(user_id)
    if user:
        return user.id
    return None

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confimation = request.form['confirmation']

        if password != confimation:
            return flash('Passwords do not match')
        else:
            supabase.auth.sign_up(email, password)
            return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'login goes here'


if __name__ == '__main__':
    app.run()

