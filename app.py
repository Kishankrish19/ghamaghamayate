from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
# Change this secret key to a complex random string when deploying to production
app.secret_key = 'ghamaghamayate_super_secret_key'

# Simple hardcoded credentials for temporary use
USER_DATABASE = {
    "admin": "password123"
}

@app.route('/')
def index():
    # If already logged in, skip login page and head to dashboard
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if username in USER_DATABASE and USER_DATABASE[username] == password:
        session['user'] = username
        return jsonify({"success": True, "redirect": url_for('dashboard')})
    
    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/dashboard')
def dashboard():
    # Secure route: redirect to login if session doesn't exist
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/api/logout', methods=['POST'])
def logout_api():
    session.pop('user', None)
    return jsonify({"success": True, "redirect": url_for('index')})

if __name__ == '__main__':
    # Runs the app locally on http://127.0.0.1:5000
    app.run(debug=True)