import logging
from itsdangerous import json
from telegram.ext import Updater, CommandHandler
import cloud.config as config
import requests


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

state_dict = {'open': 'aperti', 'close': 'chiusi'}


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Benvenuto nel bot di smart_neighborhood!')
    chat_id = update['message']['chat']['id']
    ret = requests.get("http://" + config.SERVER_IP + "houses/chat/all/")
    if ret.status_code != 200:
        raise Exception
    chats = json.loads(ret.content)['chats']
    new = True
    for chat in chats:
        if chat['chat_id'] == chat_id:
            new = False
            break
    if new:
        ret = requests.post("http://" + config.SERVER_IP + "/houses/chat/add", json={'chat_id': chat_id})
        if ret.status_code != 200:
            raise Exception

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Questo bot invia un messaggio ogni volta che il sistema smart_neighborhood apre o chiude gli scuri in modo autonomo.')
    
def send_notification(new_state):
    ret = requests.get("http://" + config.SERVER_IP + "/houses/chat/all/")
    if ret.status_code != 200:
        raise Exception
    chats = json.loads(ret.content)['chats']
    for chat in chats:
        updater.bot.send_message(chat_id=chat['chat_id'],
                                 text='Il sistema smart_neighborhood ha deciso che i tuoi scuri verrano %s. \
                                 Se vuoi gestirli manualmente utilizza la web app %s' % (state_dict[new_state], config.WEB_APP_URL))


def start_bot():
    global updater
    updater = Updater(config.BOTKEY_TELEGRAM, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    return updater


if __name__ == '__main__':
    updater = start_bot()
    updater.idle()
