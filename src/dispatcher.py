# Importing required modules
import src.inline_keyboard as ik

from aiogram import Bot, Dispatcher, executor, types
from src.config import TOKEN
from src.weather import error, get_weather, helper, weather_more, weather_week
from src.database import add_subscription, create_table

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# /start and /help message processing
@dp.message_handler(commands=['start', 'help'])
async def start(message):
    create_table()
    await message.answer(text=f'Привет, {message.from_user.first_name}!' f'{helper()}')


# /subscribe 'city' message processing (in dev, now just save user_id and city in the table)
@dp.message_handler(commands=['subscribe'])
async def subscribe(message):
    city = message.text.split(' ', maxsplit=1)[1]
    res = get_weather(city)
    if res == 0:
        await message.answer(text=error(city))
    else:
        add_subscription(message.from_user.id, city, '12:00')
        await message.answer(text=res)


# user can also take weather from command /message 'city'
@dp.message_handler(commands=['weather'])
async def weather(message):
    city = message.text.split(' ', maxsplit=1)[1]
    res = get_weather(city)

    if res == 0:
        await message.answer(text=error(city))
    else:
        await message.answer(text=res)


# the main idea of the bot is to send
# the weather to the query by the name of the city
@dp.message_handler(content_types=['text'])
async def weather(message):
    city = message.text.strip().lower()
    res = get_weather(city)

    if res == 0:
        await message.answer(text=error(city))
    else:
        await message.answer(text=res, reply_markup=ik.keyboard)


# button more
@dp.callback_query_handler(text='more')
async def process_callback_more(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None)

    await bot.answer_callback_query(callback_query.id)

    message_text = weather_more()

    await bot.send_message(
        chat_id=callback_query.message.chat.id, text=message_text, reply_markup=ik.more)


# button week
@dp.callback_query_handler(text='week')
async def process_callback_more(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None)

    await bot.answer_callback_query(callback_query.id)
    message = f'\U0001F52D Погода на пять дней:\n' f'\n{weather_week()}'
    await bot.send_message(
        chat_id=callback_query.message.chat.id, text=message, reply_markup=ik.week)


# button author
@dp.callback_query_handler(text='author')
async def author(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None)
    await bot.answer_callback_query(callback_query.id)

    message = (
        f'Контактные данные для связи:\n' f'Телеграм: @khusrabov\n' f'github: khusrabov'
    )
    await bot.send_message(
        chat_id=callback_query.message.chat.id, text=message, reply_markup=None)
