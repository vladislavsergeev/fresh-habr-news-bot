import json

import logging

import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text

from main import check_news_update

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# Настройки WebHook

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'

WEBHOOK_PATH = f'/webhook/{TOKEN}'

WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Настройки веб-сервера

WEBAPP_HOST = '0.0.0.0'

WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние пять новостей", "Обновить список новостей"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{hbold(v['article_date_time'])}\n\n" \
               f"{hlink(v['article_title'], v['article_url'])}\n\n"

        await message.answer(news)


@dp.message_handler(Text(equals="Последние пять новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(v['article_date_time'])}\n\n" \
               f"{hlink(v['article_title'], v['article_url'])}\n\n"

        await message.answer(news)


@dp.message_handler(Text(equals="Обновить новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) != 0:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(v['article_date_time'])}\n\n" \
                   f"{hlink(v['article_title'], v['article_url'])}\n\n"

        await message.answer("Список новостей успешно обновлён.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
