import logging
import json
from pyparsing import one_of
from telegram.ext import Updater, CommandHandler
import requests
import pytz
import datetime
from dateutil import parser
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.append(str(root))
import cloud.config as config


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

state_dict = {'open': 'aperti', 'close': 'chiusi'}

class BotTelegram:
    def __init__(self):
        self.updater = self.start_bot()
        self.updater.idle()
        self.state_dict = {'open': 'aperti', 'close': 'chiusi'}
        
    def start_bot(self):
        updater = Updater(config.BOTKEY_TELEGRAM, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help))

        updater.start_polling()
        return updater

    def start(self, update, context):
        update.message.reply_text('Benvenuto nel bot di smart_neighborhood!')
        chat_id = update['message']['chat']['id']
        ret = requests.get(config.WEB_APP_URL + "chat/all/")
        if ret.status_code != 200:
            raise Exception
        chats = json.loads(ret.content)['chats']
        is_new = True
        for chat in chats:
            if chat['chat_id'] == chat_id:
                is_new = False
                break
        if is_new:
            ret = requests.post(config.WEB_APP_URL + "chat/add/", json={'chat_id': chat_id})
            if ret.status_code != 200:
                raise Exception

    def help(self, update, context):
        update.message.reply_text('Questo bot invia un messaggio ogni volta che il sistema smart_neighborhood apre o chiude gli scuri in modo autonomo.')
    

def send_notification(new_state):
    ret = requests.get(config.WEB_APP_URL + "chat/all/")
    if ret.status_code != 200:
        raise Exception
    chats = json.loads(ret.content)['chats']
    for chat in chats:
        one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        local_timezone = pytz.timezone('Europe/Rome')
        one_hour_ago = local_timezone.localize(one_hour_ago)
        ultimo_messaggio = parser.parse(chat['ultimo_messaggio'])
        if ultimo_messaggio < one_hour_ago:
            text = "Il+sistema+smart\_neighborhood+ha+deciso+che+i+tuoi+scuri+verrano+%s.+Se+vuoi+gestirli+manualmente+utilizza+la+web+app+%s" % (state_dict[new_state], config.WEB_APP_URL)
            url = "https://api.telegram.org/bot" + config.BOTKEY_TELEGRAM + "/sendMessage?chat_id=" + chat['chat_id'] + "&parse_mode=Markdown&text=" + text
            ret = requests.get(url)
            if ret.status_code != 200:
                raise Exception
            ret = requests.get(config.WEB_APP_URL + "chat/update/" + chat['chat_id'] + "/")
            if ret.status_code != 200:
                raise Exception


if __name__ == "__main__":
    global updater
    bot_telegram = BotTelegram()
