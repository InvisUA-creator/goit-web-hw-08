from mongoengine import Document, StringField, EmailField, BooleanField


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField(required=False)
    sent = BooleanField(default=False)
    preferred_method = StringField(choices=['email', 'sms'], required=True)