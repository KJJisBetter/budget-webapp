from flask import Flask, request, redirect, render_template, flash, session
from config import DevelopmentConfig, ProductionConfig
from supabase import create_client
from gotrue.errors import AuthApiError
import os

app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']

if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


# Supabase client = database connection
URL = app.config['SUPABASE_URL']
KEY = app.config['SUPABASE_KEY']
supabase = create_client(URL, KEY)

session = supabase.auth.get_session()

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # print(request.form)

        email_address = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirm-password')

        if password != confirmation:
            flash('Passwords do not match')
            return redirect('/register')
        
        credentials = {
            'email': email_address,
            'password': password,
        }

        try:
            supabase.auth.sign_up(credentials)
        except AuthApiError as error:
            flash(error.message)
            return redirect('/register')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form.get('email')
        password = request.form.get('password')

        credentials = {
            'email': email_address,
            'password': password,
        }

        session = supabase.auth.sign_in_with_password(credentials)
        
    return render_template('login.html')


if __name__ == '__main__':
    app.run()

