import asyncio
import os
import sys
from typing import List

from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import logging
import mysql.connector

# from parsing_app.models import TelegramUser

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', )
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logger.error(f"start hand")
    # chat_id = message.chat.id
    # CHAT_ID = chat_id
    logger.error(f"user_id={message.from_user.id}")
    # await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Your chat ID is {CHAT_ID}, userid {message.from_user.id}")


async def send_notification(message, chat_id=CHAT_ID):
    try:
        await bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
    except TelegramForbiddenError as e:
        logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def get_products_from_database() -> List[str]:
    # Настройки подключения к базе данных
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '1111',
        'database': 'parser'
    }

    # Подключение к базе данных
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Выполнение запроса к базе данных
    query = "SELECT * FROM parsing_app_lastproducts"
    cursor.execute(query)

    # Получение результатов запроса
    products = [row for row in cursor.fetchall()]

    # Закрытие соединения с базой данных
    cursor.close()
    connection.close()

    logger.warning(products)

    return products


def format_product_list(products: List[str]) -> str:
    product_list_text = ""
    for index, product in enumerate(products, start=1):
        product_list_text += f"{index}. Название: {product[1]}\nСсылка на изображение: {product[2]}\n"
    return product_list_text


@dp.message(Command('list'))
async def list_products(message: Message):
    logger.error(f"list_products")
    products = get_products_from_database()
    logger.error(f"products")
    response_text = format_product_list(products)
    logger.error(f"formed list")
    if response_text:
        await message.answer(response_text)
    await message.answer("Пустой список")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        # CHAT_ID = message.chat.id
        # await message.send_copy(chat_id=message.chat.id) Изпользуем чтобы получить наш chat_id
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    logger.error(f"Пришло в main()")
    await dp.start_polling(bot)
    logger.error(f"Запустилось в main()")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.error(f"Запустилось в if main")
    asyncio.run(main())


def start_bot():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.error(f"Запустилось в start_bot")
    asyncio.run(main())


