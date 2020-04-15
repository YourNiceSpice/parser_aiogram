import logging
from aiogram import Bot, Dispatcher, executor, types
import follow_add_proxy

bot = Bot(token = '1043923109:AAG26SjtlMZLd5mmPt78D8Fch7vYnlTCPoM')

dispatcher = Dispatcher(bot)

@dispatcher.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    запускаем парсер
    """
    await message.answer("Запускаем парсер:/stop,чтобы остановить")
    global start_follow
    start_follow = True
    while start_follow:
        try:
            await message.answer(follow_add_proxy.main())
        except Exception as e:
            print(e)
@dispatcher.message_handler(commands=['stop'])
async def send_buy(message: types.Message):
    global start_follow
    start_follow = False
    follow_add_proxy.del_list()
    await message.answer('Buy')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)