from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Criação da instância do aplicativo Flask
app = Flask(__name__)

# Chave secreta necessária para o gerenciamento de sessões do Flask-Login
app.secret_key = 'supersecretkey'  # Substitua por uma chave secreta mais segura em produção

# Caminho do arquivo de registro de usuários
USER_FILE = 'users.txt'

# Inicializando o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define a página de login para redirecionamento

# Função para obter dados de usuários do arquivo
def get_user_data():
    if not os.path.exists(USER_FILE):  # Verifica se o arquivo de usuários existe
        return []
    with open(USER_FILE, 'r') as f:
        return [line.strip().split(',') for line in f]  # Lê os dados de usuários

# Função para registrar um novo usuário
def register_user(username, password):
    hashed_password = generate_password_hash(password)  # Criptografa a senha
    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")  # Armazena o usuário e senha criptografada

# Função para verificar se um usuário existe
def user_exists(username):
    users = get_user_data()  # Obtém todos os usuários registrados
    for existing_username, _ in users:
        if existing_username == username:
            return True
    return False

# Função para obter um usuário a partir do nome de usuário
def get_user_by_username(username):
    users = get_user_data()  # Obtém todos os usuários
    for existing_username, hashed_password in users:
        if existing_username == username:
            return User(existing_username, hashed_password)  # Retorna um objeto User
    return None

# Classe User para integração com o Flask-Login
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
    
    def get_id(self):
        return self.username  # Retorna o id (username) do usuário
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Verifica se a senha bate com o hash

# Função para carregar o usuário com Flask-Login
@login_manager.user_loader
def load_user(username):
    return get_user_by_username(username)  # Carrega o usuário pelo nome de usuário

@app.route('/')
def index():
    # Página inicial redireciona para login se o usuário não estiver autenticado
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Se o formulário de login for enviado
        # Obtém os valores inseridos pelo usuário
        entered_username = request.form.get('username')
        entered_password = request.form.get('password')

        user = get_user_by_username(entered_username)  # Tenta encontrar o usuário pelo nome

        # Verifica se o usuário existe e se a senha está correta
        if user and user.check_password(entered_password):
            login_user(user)  # Faz o login do usuário
            return redirect(url_for('home'))  # Redireciona para a página home
        return render_template('login.html', error="Usuário ou senha incorretos. Tente novamente.")  # Se as credenciais estiverem erradas

    return render_template('login.html', error=None)  # Exibe o formulário de login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Se o formulário de registro for enviado
        username = request.form.get('username')
        password = request.form.get('password')

        # Verifica se o usuário já existe
        if user_exists(username):
            return render_template('register.html', error="Usuário já existe. Escolha outro nome de usuário.")
        
        # Registra o novo usuário
        register_user(username, password)
        return redirect(url_for('login'))  # Redireciona para a página de login

    return render_template('register.html', error=None)  # Exibe o formulário de registro

@app.route('/home')
@login_required  # Página protegida que exige que o usuário esteja logado
def home():
    return render_template('home.html', username=current_user.username)  # Exibe a página home com o nome do usuário

@app.route('/logout')
@login_required  # Página protegida que exige que o usuário esteja logado
def logout():
    logout_user()  # Faz o logout do usuário
    return redirect(url_for('login'))  # Redireciona para a página de login

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo em modo de debug
