from mongoengine import Document, StringField, ListField, ReferenceField


class Author(Document):
    full_name = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote_text = StringField(required=True)