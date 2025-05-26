from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'mi_token_de_verificacion'  # Usa este mismo en Facebook
PAGE_ACCESS_TOKEN = '37101d0500b6872e781ba0b57d4f33dc'  # Reemplaza con tu token real

@app.route('/', methods=['GET'])
def verify():
    token_sent = request.args.get("hub.verify_token")
    return request.args.get("hub.challenge") if token_sent == VERIFY_TOKEN else 'Token inválido'

@app.route('/', methods=['POST'])
def receive_message():
    body = request.get_json()
    for event in body['entry']:
        messaging = event['messaging']
        for message_event in messaging:
            if 'message' in message_event:
                sender_id = message_event['sender']['id']
                message_text = message_event['message'].get('text')
                if message_text:
                    send_message(sender_id, f"Hola, recibí tu mensaje: {message_text}")
    return "ok", 200

def send_message(recipient_id, text):
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    auth = {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.post('https://graph.facebook.com/v17.0/me/messages',
                             params=auth, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)