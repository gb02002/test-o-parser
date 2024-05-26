from django.core.management.base import BaseCommand
import asyncio
from management.management.bot import bot


class Command(BaseCommand):
    help = 'Start of bot'

    def handle(self, *args, **options):
        asyncio.run(bot.polling())

