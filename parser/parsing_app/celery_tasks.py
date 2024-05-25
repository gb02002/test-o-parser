import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from celery import Celery, shared_task
from parsing_app.models import Products

from parser.settings import REDIS_HOST, REDIS_PORT

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@celery.task
def start_parsing(amount_of_products):
    """Main logic"""
    pass
