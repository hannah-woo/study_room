# import sys
# sys.path.append('../folder_crwaling') if crawling file exists in other folder
from crawler import get_code, get_sise, get_news
import openpyxl
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pandas
import dataframe_image as dfi

# 텔레그램 정보 가져오기
telegram_config = {}
with open('telegram_config', 'r') as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.rstrip().split('=')
        telegram_config[key] = value
token = telegram_config['token']
chat_id = telegram_config['chatId']
    
# 텔레그램 봇 생성하기
bot = telegram.Bot(token)

# updater & dispatcher 설정하기
updater = Updater(token, use_context = True)
dispatcher = updater.dispatcher

# polling 시작
updater.start_polling()

def handler(update, context):
    user_text = update.message.text
    if user_text == '종료':
        bot.send_message(chat_id, '종료합니다.')
    else:
        try:
             # 주식가격 가져오기
            company_code = get_code(user_text)
            company_sise = get_sise(company_code)
            dfi.export(company_sise, 'sise.png', max_cols = -1, max_rows = -1)
            bot.send_message(chat_id, '%s의 주식가격을 가져옵니다.' %user_text)
            with open('./sise.png', 'rb') as f:
                bot.send_photo(chat_id, f)

            # 뉴스 가져오기
            company_news = get_news(company_code)
            dfi.export(company_news, 'news.png', max_cols = -1, max_rows = -1)
            bot.send_message(chat_id, '%s의 최신 뉴스를 가져옵니다.' %user_text)
            with open('./news.png', 'rb') as f: 
                bot.send_photo(chat_id, f)         
        except Exception as e:
                print(e)
                bot.send_message(chat_id, '정보를 가져올 수 없습니다. 다시 확인해주십시오.')

echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)