import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


API_TOKEN = '7240941938:AAG_4I_UweAJDqVy3SgDPjizNn3SDgB1L-4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(commands=['start'
                              ''])
async def start(message: types.Message):
    await message.answer('Привет! Напишите "Calories", чтобы начать расчет нормы калорий.')


@dp.message_handler(lambda message: message.text.lower() == 'calories')
async def set_gender(message: types.Message):
    await UserState.gender.set()
    await message.answer('Введите ваш пол (мужчина/женщина):')


@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender in ['мужчина', 'женщина']:
        await state.update_data(gender=gender)
        await UserState.age.set()
        await message.answer('Введите свой возраст:')
    else:
        await message.answer('Пожалуйста, введите корректный пол (мужчина/женщина).')


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await UserState.growth.set()
        await message.answer('Введите свой рост (в см):')
    else:
        await message.answer('Пожалуйста, введите корректный возраст (число).')


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(growth=message.text)
        await UserState.weight.set()
        await message.answer('Введите свой вес (в кг):')
    else:
        await message.answer('Пожалуйста, введите корректный рост (число)')


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        await state.update_data(weight=message.text)
        data = await state.get_data()

        if 'gender' in data and 'age' in data and 'growth' in data and 'weight' in data:
            gender = data['gender']
            age = int(data['age'])
            growth = int(data['growth'])
            weight = int(data['weight'])

            if gender == 'мужчина':
                calories = 66.5 + (13.75 * weight) + (5.003 * growth) - (6.75 * age)

            elif gender == 'женщина':
                calories = 655.1 + (9.563 * weight) + (1.850 * growth) - (4.676 * age)

            else:
                await message.answer('Ошибка: некорректный пол.')
                return

            await message.answer(f'Ваша норма калорий: {calories:.2f} ккал.')

        else:
            await message.answer('Ошибка: недостающие данные для расчета калорий.')

        await state.finish()
    else:
        await message.answer('Пожалуйста, введите корректный вес (число).')


if __name__ == '__main__':
    print('Бот запущен. Ожидаение сообщений...')
    executor.start_polling(dp, skip_updates=True)
