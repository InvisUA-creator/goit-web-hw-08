import pika
from models import Contact
from connect import connect_to_mongo


connect_to_mongo()

def send_email(contact):
    print(f'Пошта надіслана: {contact.email}')


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.send:
        send_email(contact)
        contact.send = True
        contact.save()
        print(f'Оновлено статус пошти для контакта {contact_id}')


credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        credentials=credentials)
    )

channel = connection.channel()

channel.queue_declare(queue='send_email_queue')

channel.basic_consume(queue='send_email_queue', on_message_callback=callback, auto_ack=True)

print('Очікування на повідомлення...')

channel.start_consuming()
