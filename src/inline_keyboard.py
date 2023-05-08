# Importing required modules
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Creating an instance of InlineKeyboardMarkup
keyboard = InlineKeyboardMarkup()

# Creating buttons and adding them to the keyboard
button_more = InlineKeyboardButton('Подробнее', callback_data='more')
button_subscribe = InlineKeyboardButton('Автор', callback_data='author')
button_week = InlineKeyboardButton('На пять дней', callback_data='week')
keyboard.row(button_more, button_week, button_subscribe)

# Creating another instance of InlineKeyboardMarkup for the "Подробнее" button
more = InlineKeyboardMarkup()
more.row(InlineKeyboardButton('На пять дней', callback_data='week'))
more.row(InlineKeyboardButton('Автор', callback_data='author'))

# Creating another instance of InlineKeyboardMarkup for the "На пять дней" button
week = InlineKeyboardMarkup()
week.row(InlineKeyboardButton('Автор', callback_data='author'))
