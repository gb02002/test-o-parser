import asyncio
from aiogram.enums.parse_mode import ParseMode
from celery import Celery, shared_task
from .models import TelegramUser, LastProducts

from parsing_app.core import main_logic
import logging
from parser.settings import REDIS_HOST, REDIS_PORT
from management.management.bot import bot, send_notification

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

celery = Celery('celery_tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@celery.task
def start_parsing(amount_of_products):
    """Main logic"""
    LastProducts.objects.all().delete()
    result = main_logic(amount_of_products)
    if result:
        send_telegram_message.delay(amount_of_products)


@shared_task
def send_telegram_message(n):
    """Notification"""
    # chat_id = TelegramUser.objects.all()[0]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(send_message(f'Задача на парсинг товаров с сайта Ozon завершена. '
                                                      f'Сохранено {n} товаров.'))
    except Exception as e:
        logger.error(f"Error sending message via Celery task: {e}")


async def send_message(message):
    await send_notification(message)
