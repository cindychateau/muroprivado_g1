from flask import render_template, redirect, session, request, flash #importaciones de módulos de flask
from flask_app import app

#Importando el Modelo de User
from flask_app.models.users import User
#Importando el modelo de Messages
from flask_app.models.messages import Message

#Importando BCrypt (encriptar)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) #inicializando instancia de Bcrypt

@app.route('/')
def index():
    return render_template('index.html')

#Creando una ruta para /register
@app.route('/register', methods=['POST'])
def register():
    #request.form = {
    #   "first_name": "Elena",
    #   "last_name": "De Troya",
    #   "email": "elena@cd.com",
    #   "password": "123456",
    #}
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) #Me encripta el password

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Guardando a mi usuario y recibo el ID del nuevo registro

    session['usuario_id'] = id #Guardando en sesion el identificador

    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user: #si user=False
        flash("E-mail no encontrado", 'login')
        return redirect('/')
    
    #Comparando la contraseña encriptada con la contraseña del LOGIN
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", 'login')
        return redirect('/')
    
    session['usuario_id'] = user.id

    return redirect('/wall')

@app.route('/wall')
def wall():
    if 'usuario_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario) #El usuario que inicio sesión

    users = User.get_all() #Lista de todos los usuarios

    messages = Message.get_user_messages(formulario)

    return render_template('wall.html', user=user, users=users, messages=messages)

@app.route('/logout')
def logout():
    session.clear() #Elimine la sesión
    return redirect('/')