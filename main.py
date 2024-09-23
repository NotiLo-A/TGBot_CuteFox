
import asyncio
from random import choice
from random import *
from urllib.error import HTTPError

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from urllib.request import urlopen, Request
from bs4 import *


FOXES_DIR_LINK = "https://wohlsoft.ru/images/foxybot/foxes/"


def http_get(url: str):
    request = Request(url)
    try:
        with urlopen(request) as response:
            data = response.read()
            return {
                "data": data,
                "status": response.status,
                "url": response.url
            }
    except HTTPError as error:
        return {
            "status": error.code,
        }


def get_foxes():
    data = http_get(FOXES_DIR_LINK)["data"]
    parsed_html = BeautifulSoup(data)
    links = []
    for link in parsed_html.body.find_all('td', attrs={'class':'indexcolname'})[1:]:
        links.append(FOXES_DIR_LINK + link.a.get("href"))
    return links


bot = Bot(token='7852413770:AAGvS6GCvcbadVS6OsxvXIuwKGW98HjNZA8')
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('привет')


@dp.message(Command('FoxPic'))
async def foxpic(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=choice(get_foxes()))



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

