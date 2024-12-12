import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


API_TOKEN = ""


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('Привиет! Я бот помогающий твоему здоровью.')
    await message.answer('Привиет! Я бот помогающий твоему здоровью.')


@dp.message_handler(lambda message: True)
async def all_messages(message: types.Message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    print('Бот запущен. Ожидает сообщений...')
    executor.start_polling(dp, skip_updates=True)
