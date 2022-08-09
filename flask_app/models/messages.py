from flask_app.config.mysqlconnection import connectToMySQL

class Message:

    def __init__(self, data):
        #Vamos a poner todos las propiedades que la instancia de Message va a tener
        #{id: 1, content: "¿Qué tal", receiver_id:1, sender_id:2, cr..up..., receiver_name:"Elena", sender_name:"Juana" }
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        #No tenemos en las columnas pero que vamos a poder obtener gracias al query
        self.sender_name = data['sender_name']
        self.receiver_name = data['receiver_name']
    
    @classmethod
    def save(cls, formulario):
        #formulario = {content: "mensaje", sender_id: ID del que manda, receiver_id: ID del que va a recibir}
        query = "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s) "
        result = connectToMySQL('muroprivado_g1').query_db(query, formulario)
        return result
    
    @classmethod
    def get_user_messages(cls, formulario):
        #formulario = {id: 1}
        query = "SELECT messages.*, senders.first_name as sender_name, receivers.first_name as receiver_name FROM messages LEFT JOIN users as senders ON senders.id = sender_id LEFT JOIN users as receivers ON receivers.id = receiver_id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('muroprivado_g1').query_db(query, formulario)
        #results = [
        #   {id: 1, content: "¿Qué tal", receiver_id:1, sender_id:2, cr..up..., receiver_name:"Elena", sender_name:"Juana" }
        #]
        messages = []
        for message in results:
            messages.append(cls(message)) #1.- cls(message) crea instancia de mensaje. 2.- ingreso esa instancia a mi lista
        return messages

    @classmethod
    def destroy(cls, formulario):
        #formulario = {id: 1}
        query = "DELETE FROM messages WHERE id = %(id)s"
        result = connectToMySQL('muroprivado_g1').query_db(query, formulario)
        return result
