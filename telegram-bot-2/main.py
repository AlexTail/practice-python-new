"""

№ 2 Простой бот для Telegram, который определяет ID пользователя, содержит
меню из одной команд и дублирует текст, который написал пользователь.

№ 2 A simple Telegram bot that identifies the user ID contains
A menu of one command and duplicates the text that the user wrote.

"""


from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters 

from config import TG_TOKEN 
from config import TG_API_URL


def do_start(bot: Bot, update: Update):
    try:
        bot.send_message(
            chat_id = update.message.chat_id,
            text = 'Привет! Напиши мне что-нибудь.'
        )
    except Exception as ex:
        print('do_start: ', ex)
    print('do_start: done')


def do_help(bot: Bot, update: Update):
    try:
        bot.send_message(
            chat_id = update.message.chat_id,
            text = 'Это учебный бот\n'
                   'Список доступных команд, есть в меню\n'
                   'А также продублирую текст в ответ',
        )
    except Exception as ex:
        print('do_start: ', ex)

    print('do_help: done')


def do_echo(bot: Bot, update: Update):
    try:
        chat_id = update.message.chat_id
        text = "Ваш ID = {}\n\n{}".format(chat_id, update.message.text)
        
        bot.send_message( 
                chat_id = chat_id,
                text = text,
        )
    except Exception as ex:
        print('do_echo: ', ex)
    
    print('do_echo: done')


def main():
    try:
        bot = Bot(
            token = TG_TOKEN,
            base_url = TG_API_URL,
        )
        updater = Updater(
            bot = bot,
        )
        
        start_handler = CommandHandler("start", do_start)
        help_handler = CommandHandler("help", do_help)
        message_handler = MessageHandler(Filters.text, do_echo)
        
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(help_handler)
        updater.dispatcher.add_handler(message_handler)
        
        updater.start_polling()
        updater.idle()
    except Exception as ex:
        print('main: ', ex)


if __name__ == '__main__':
    print('go')
    main()