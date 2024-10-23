import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()
def connect_mongo():
    connect(
        db=os.getenv("MONGO_DB"),
        host=f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@cluster0.hqwgv.mongodb.net/mydatabase?retryWrites=true&w=majority",
        ssl=True
    )