import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

health_facts = [
    "Регулярные физические упражнения могут улучшить ваше настроение.",
    "Питье достаточного количества воды помогает поддерживать здоровье кожи.",
    "Сон важен для восстановления и общего самочувствия.",
    "Сбалансированное питание способствует улучшению работы мозга.",
    "Стресс может негативно сказаться на вашем здоровье, поэтому важно находить время для отдыха."
]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью. Используй команду /fact,'
                         ' чтобы получить интересный факт о здоровье!')


@dp.message_handler(commands=['fact'])
async def send_health_fact(message: types.Message):
    fact = random.choice(health_facts)
    await message.answer(f'Вот интересный факт: {fact}')


@dp.message_handler(lambda message: True)
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение или /fact, чтобы '
                         'получить интересный факт о здоровье.')


if __name__ == '__main__':
    print("Бот запущен. Ожидает сообщений...")
    executor.start_polling(dp, skip_updates=True)