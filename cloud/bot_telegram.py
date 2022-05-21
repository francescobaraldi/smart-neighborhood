import logging
import json
from telegram.ext import Updater, CommandHandler
import requests
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.append(str(root))
import cloud.config as config


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
    
    def send_notification(self, new_state):
        ret = requests.get(config.WEB_APP_URL + "chat/all/")
        if ret.status_code != 200:
            raise Exception
        chats = json.loads(ret.content)['chats']
        for chat in chats:
            self.updater.bot.send_message(chat_id=chat['chat_id'],
                                    text='Il sistema smart_neighborhood ha deciso che i tuoi scuri verrano %s. \
                                    Se vuoi gestirli manualmente utilizza la web app %s' % (self.state_dict[new_state], config.WEB_APP_URL))


def get_bot_telegram():
    global bot_telegram 
    return bot_telegram

if __name__ == "__main__":
    global updater
    bot_telegram = BotTelegram()
