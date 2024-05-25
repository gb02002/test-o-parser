from celery import Celery

from parsing_app.core import main_logic

from parser.settings import REDIS_HOST, REDIS_PORT

celery = Celery('celery_tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@celery.task
def start_parsing(amount_of_products):
    """Main logic"""
    main_logic(amount_of_products)
