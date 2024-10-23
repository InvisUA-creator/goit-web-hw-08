import json
import redis
import logging
from models import Author, Quotes
from connect import connect_mongo


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    connect_mongo()
    logging.info("MongoDb підключено успішно.")
except Exception as e:
    logging.error(f"Помилка підключення до MongoDb: {e}")


try:
    r = redis.StrictRedis(host="localhost", port=6379, db=0, socket_timeout=12)
    logging.info("Redis підключено успішно.")
except Exception as e:
    logging.error(f"Помилка підключення до Redis: {e}")


def fetch_quotes_to_author(author_name):
    logging.info(f"Пошук цитат для автора: {author_name}")
    try:
        author = Author.objects(fullname__icontains=author_name).first()
        if author:
            author_ids = [author.id for author in authors]
            quotes = Quotes.objects(author__in=author_ids)
            logging.info(f"Знайдено {len(quotes)} цитат для автора {author_name}.")
            return quotes
        logging.warning(f"Автор {author_name} не знайдено.")
        return None
    except Exception as e:
        logging.error(f"Помилка при завантаженні цитат автора: {e}")
        return None


def fetch_quotes_to_tag(tag_name):
    logging.info(f"Пошук цитат для тега: {tag_name}")
    try:
        quotes = Quotes.objects(tags__in=tag_name)
        logging.info(f"Знайдено {len(quotes)} цитат для тега {tag_name}.")
        return quotes
    except Exception as e:
        logging.error(f"Помилка при завантаженні цитат за тегом: {e}")
        return None


def fetc_quotes_to_tags(tag_list):
    logging.info(f"Пошук цитат для списку тегів: {tag_list}")
    try:
        quotes = Quotes.objects(tags__in=tag_list)
        logging.info(f"Знайдено {len(quotes)} цитат для списку тегів {tag_list}.")
        return quotes
    except Exception as e:
        logging.error(f"Помилка при завантаженні цитат за списком тегів: {e}")
        return None


def cache_result(key, result):
    try:
        r.set(key, json.dumps(result), ex=360)
        logging.info(f"Збережено результат до кеша з ключем: {key}")
    except Exception as e:
        logging.error(f"Помилка при збереженні результату до кеша: {e}")


def get_cache_result(key):
    try:
        result = r.get(key)
        if result:
            logging.info(f"Знайдено результат з кеша з ключем: {key}")
            return json.loads(result)
        return None
    except Exception as e:
        logging.error(f"Помилка при завантаженні результату з кеша: {e}")
        return None


def search_quotes(command):
    try:
        if command.startswith("name:"):
            author_name = command.split(":", 1)[1].strip()
            if len(author_name) < 3:
                logging.warning(f"Непридатний набір символів для автора: {author_name}")
                return []

            cache_quotes = get_cache_result(f"name:{author_name}")
            if cache_quotes:
                result = "\n".join(cache_quotes)
                logging.info(f"Знайдено результат з кеша для автора {author_name}.")
                return result

            quotes = fetch_quotes_to_author(author_name)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
                cache_result(f"name:{author_name}", [q.quote for q in quotes])
            else:
                result = "Автор не знайдений."

        elif command.startswith("tag:"):
            tag_name = command.split(":", 1)[1].strip()
            if len(tag_name) < 3:
                logging.warning(f"Непридатний набір символів для тега: {tag_name}")
                return []

            cache_quotes = get_cache_result(f"tag:{tag_name}")
            if cache_quotes:
                result = "\n".join(cache_quotes)
                logging.info(f"Знайдено результат з кеша для тега {tag_name}.")
                return result

            quotes = fetch_quotes_to_tag(tag_name)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
                cache_result(f"tag:{tag_name}", [q.quote for q in quotes])
            else:
                result = "Тег не знайдений."

        elif command.startswith("tags:"):
            tag_list = command.split(":", 1)[1].strip().split(",")
            tag_list = [tag.strip() for tag in tags if len(tag.strip()) >= 2]

            if not tag_list:
                print("Всі теги короткі.")
                return []

            quotes = fetc_quotes_to_tags(tags)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
            else:
                print("Теги не знайдені.")

        elif command == "exit":
            logging.info("Завершення роботи.")
            print("Завершення.")
            return

        else:
            logging.warning("Невірна команда.")
            print("Невірна команда.")

    except Exception as e:
        logging.error(f"Помилка при пошуку цитат: {e}")
        print("Помилка при пошуку цитат.")


while True:
    command = input("Введіть команду: ")
    search_quotes(command)
