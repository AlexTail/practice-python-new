"""

Простой бот для Telegram, который определяет имя пользователя и координаты
фотографии (которая была отправлена как файл) - если они не удалены у фото.

A simple Telegram bot that defines the username and coordinates
photos (which was sent as a file) - if they are not deleted from the photo.

"""



from io import BytesIO
from pprint import pprint

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

import bot_config
from exif_reader import get_exif_data, get_location



def hello_world(bot, update):
    try:
        user_first_name = update.message.from_user.first_name
        update.message.reply_text(f'HelloNew1, {user_first_name}')
        print('Done - hello_world')
    
    except Exception as ex:
        print('hello_world', ex)


def reply_to_photo_file(bot, update):
    try:
        document = update.message['document']
        file_id = document['file_id']
        mime_type = document['mime_type']
        
        if mime_type.startswith('image'):
            file_info_link = f'https://api.telegram.org/bot{bot_config.TOKEN}/getFile?file_id={file_id}'
            file_path = requests.get(file_info_link, proxies={'https': bot_config.HTTPS_PROXY}).json()['result']['file_path']
            file_link = f'https://api.telegram.org/file/bot{bot_config.TOKEN}/{file_path}'
            file = requests.get(file_link,  proxies={'https': bot_config.HTTPS_PROXY}).content
            file_data = BytesIO(file)
            exif_data = get_exif_data(file_data)
            lat, lon = get_location(exif_data)
       
            update.message.reply_text(f"Location info: {lat}, {lon}")
        else:
            update.message.reply_text('Я понимаю только файлы с картинками')
        print('done - reply_to_photo_file')
        
    except Exception as ex:
        print('reply_to_photo_file', ex)


def main():
    try:
        my_bot = Updater(bot_config.TOKEN, request_kwargs={
            'proxy_url': bot_config.SOCKS_PROXY
        })
    
        dp = my_bot.dispatcher
       
        dp.add_handler(CommandHandler('start', hello_world))
        dp.add_handler(MessageHandler(Filters.document, reply_to_photo_file))
        
        my_bot.start_polling()
        my_bot.idle()

    except Exception as ex:
        print('main:', ex)


if __name__ == '__main__':
    main()   