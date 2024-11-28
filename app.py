# codigo igual o em js, mas em python #

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Credenciais corretas
valid_username = "Emizinha"
valid_password = "Emizinha123"

@app.route('/')
def login():
    return render_template('login.html', error=None)

@app.route('/login', methods=['POST'])
def login_post():
    # Obtém os valores inseridos pelo usuário
    entered_username = request.form.get('username')
    entered_password = request.form.get('password')

    # Verifica se as credenciais são válidas
    if entered_username == valid_username and entered_password == valid_password:
        return redirect(url_for('home'))
    else:
        # Retorna à página de login com mensagem de erro
        return render_template('login.html', error="Usuário ou senha incorretos. Tente novamente.")

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
