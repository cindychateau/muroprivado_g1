from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importamos modelo de Message
from flask_app.models.messages import Message

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'usuario_id' not in session:
        return redirect('/')
    
    #Guardar el formulario que recibimos
    #request.form = {content: "mensaje", sender_id: 1, receiver_id: 2}
    Message.save(request.form)
    return redirect('/wall')

@app.route('/eliminar/mensaje/<int:id>') #Id del mensaje se recibe a través de URL
def eliminar_mensaje(id):
    formulario = { "id": id } #Creamos diccionario con ese ID
    Message.destroy(formulario)
    return redirect ('/wall')