from flask import Flask, render_template, request, redirect, url_for, jsonify
from auth import generate_token, token_required

app = Flask(__name__)
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # Generar el token
            token = generate_token(user_id=username)
            return render_template('welcome.html', username=username, token=token)

        return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('register.html', error="Campos requeridos")
        if username in users:
            return render_template('register.html', error="Usuario ya existe")

        users[username] = password
        # Generar token después de registrarse
        token = generate_token(user_id=username)
        return render_template('welcome.html', username=username, token=token)
    return render_template('register.html')

@app.route('/public')
def public():
    return jsonify({'message': 'Este es un endpoint público, accesible para todos'})

@app.route('/private')
@token_required
def private(user_id):
    return jsonify({'message': f'Acceso privado para {user_id}'})

if __name__ == '__main__':
    app.run(debug=True)
