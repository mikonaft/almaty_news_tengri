import json
import random
from os import system
from time import sleep
from datetime import datetime

# imported modules
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton 

#созданные нами модули
from core.config import TOKEN, ADMIN_ID, ADMIN_ID_INT, DOMEN, URL
from core.static.stickers import S001, S002
from core.news import NewsAlmatyParser

system('clear')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_start_command(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Зарегистрироваться', request_contact=True)
    )
    photo_start = open('core/static/almaty.jpg', "rb")
    await message.reply_photo(photo=photo_start, caption="Свежие новости Алматы и главные события в городе на сегодня ✅\n Последние криминальные новости ➜ Только актуальная информация про последние события и происшествия в\n Алматы на t.me/News_Fresh_Fish_Bot!", reply_markup=markup)
    await message.answer(text="Просим вас пройти регистрацию, для того чтобы вы могли пользоваться нашим ботом")
    await message.delete()
    
@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def registration(message: types.Message):
    user_id = message.contact.user_id
    username = message.chat.username
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone = message.contact.phone_number
    
    information = f'''id: {user_id}
username: {username}
first_name: {first_name}
last_name: {last_name}
phone: {phone}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
    await bot.send_message(ADMIN_ID, information)
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('все новости'),
        KeyboardButton('свежие новости'),
        KeyboardButton('старые новости')
    )
    await message.reply_sticker(random.choice(S002))
    await message.answer('Вы успешно зарегистрированы', reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def news_today(message: types.Message):
    with open('core/json/news_almaty.json', 'r') as file:
            all_news = json.load(file)
    if message.text.lower() == 'запросить новости на сегодня':
        NewsAlmatyParser()
        news_almaty = []
        for item in all_news[:3]:
            item_title = item['title']
            item_url = item['url']
            text = f'''{item_title}\n
{item_url}'''
            await message.answer(text=text)
    elif message.text.lower() == 'свежие новости':
        NewsAlmatyParser()
        with open('core/json/news_almaty.json', 'r') as file:
            all_news = json.load(file)
        news_almaty = []
        for item in all_news[:3]:
            item_title = item['title']
            item_url = item['url']
            text = f'''{item_title}\n
{item_url}'''
            await message.answer(text=text)
        await message.reply_sticker(random.choice(S002))
        await message.answer('все новости на сегодня прочитаны')
    elif message.text.lower() == 'старые новости':
        NewsAlmatyParser()
        news_almaty = []
        for item in all_news[-3:]:
            item_title = item['title']
            item_url = item['url']
            text = f'''{item_title}\n
{item_url}'''
            await message.answer(text=text)
        await message.reply_sticker(random.choice(S002))
        await message.answer('все новости на сегодня прочитаны')
    else:
        await message.reply('UNKNOWN COMMAND')

if __name__ == '__main__':
    print("Бот запущен")
    executor.start_polling(dp)
