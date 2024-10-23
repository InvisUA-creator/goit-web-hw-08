import pika
import random
from faker import Faker
from models import Contact
from connect import connect_to_mongo


fake = Faker()
connect_to_mongo()


credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')


def generate_fake_contact():
    fullname = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    preffered_method = random.choice(['email', 'sms'])
    contact = Contact(
        fullname=fullname,
        email=email,
        phone_number=phone_number,
        preffered_method=preffered_method
        )
    contact.save()
    return contact


for _ in range(10):
    contact = generate_fake_contact()
    message = str(contact.id)
    if contact.preffered_method == 'email':
        channel.basic_publish(exchange='', routing_key='email_queue', body=message)
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=message)


print('Всі контакти у черзі.')
connection.close()
