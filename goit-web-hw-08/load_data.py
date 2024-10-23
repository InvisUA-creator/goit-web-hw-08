import json
import logging
from mongoengine import connect
from models import Author, Quotes
from connect import connect_mongo


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('load_data.log'),
        logging.StreamHandler()
    ]
)

try:
    connect_mongo()
    logging.info("Підключення до MongoDB завершено успішно")
except Exception as e:
    logging.error(f"Підключення до MongoDB з помилкою: {e}")
    exit()

try:
    with open('authors.json', encoding='utf-8') as f:
        authors_data = json.load(f)
        for author in authors_data:
            new_author = Author(
                fullname=author['fullname'],
                born_date=author['born_date'],
                born_location=author['born_location'],
                description=author['description']
            )
            new_author.save()
            logging.info(f"Автор {author['fullname']} успішно збережений")
except Exception as e:
    logging.error(f"Помилка збереження автора: {e}")


try:
    with open('quotes.json', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for quote in quotes_data:
            author=Author.objects(fullname=quote['author']).first()
            if author:
                new_quote = Quote(
                    tags = quote['tags'],
                    author = author,
                    quote_text = quote['quote']
                )
                new_quote.save()
                logging.info(f"Цитата автора {author.fullname} успішно збережена")
            else:
                logging.warning(f"Автора {quote['author']} не знайдено")
except Exception as e:
    logging.error(f"Помилка збереження цитати: {e}")


logging.info("Закриття з'єднання з MongoDB")