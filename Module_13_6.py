import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


inline_keyboard = InlineKeyboardMarkup(row_width=1)
button_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_keyboard.add(button_calories, button_formulas)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.\nВыберите действие:',
                         reply_markup=inline_keyboard)


@dp.message_handler(lambda message: message.text == 'Рассчитат')
async def mein_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formulas_text = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5\n"
        "Для женщин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) - 161"
    )
    await call.message.answer(formulas_text)


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_gender(call: types.CallbackQuery):
    await UserState.gender.set()
    await call.message.answer('Введите ваш пол (мужчина/женщина):')


@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender in ['мужчина','женщина']:
        await state.update_data(gender=gender)
        await UserState.age.set()
        await message.answer('Введите свой возрост:')
    else:
        await message.answer('Пожалуйста, введите корректный пол (мужчина/женщина).')


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await UserState.growth.set()
        await message.answer('Введите свой рост (в см):')
    else:
        await message.answer('Пожалуйста, введите коррктный возраст (число).')


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(growth=message.text)
        await UserState.weight.set()
        await message.answer('Введите свой вес (в кг):')
    else:
        await message.answer('Пожалуйста, введите коррктный рост (число).')


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
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


@dp.message_handler(lambda message: message.text == 'Информация')
async def send_info(message: types.Message):
    info_text = (
            "Этот бот поможет вам рассчитать вашу норму калорий на основе ваших параметров.\n"
            "Введите ваш пол, возраст, рост и вес, и бот предоставит вам информацию о вашей норме калорий.\n"
            "Нажмите 'Рассчитать', чтобы начать!"
        )
    await message.answer(info_text)


if __name__ == '__main__':
    print('Бот запущен. Ожидание сообщений...')
    executor.start_polling(dp, skip_updates=True)


