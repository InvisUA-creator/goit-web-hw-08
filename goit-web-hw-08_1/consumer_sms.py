import pika
from models import Contact
from connect import connect_to_mongo

connect_to_mongo()


def send_sms(contact):
    print(f'SMS надіслано: {contact.phone_number}')


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.sent:
        send_sms(contact)
        contact.sent = True
        contact.save()
        print(f'Запис з id {contact_id} відправлено SMS')


credentials = pika.PlainCredentials('user', 'password')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        credentials=credentials
    )

channel = connection.channel()

channel.queue_declare(queue='sms_queue')

channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Слухаючий режим запущений...')

channel.start_consuming()