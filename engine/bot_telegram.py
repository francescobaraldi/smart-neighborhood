import logging
from telegram.ext import Updater, CommandHandler
from .config import BOTKEY_TELEGRAM, WEB_APP_URL


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

chat_ids = [] # La lista delle chat va salvata nel db in modo permanente
state_dict = {'open': 'aperti', 'close': 'chiusi'}


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Benvenuto nel bot di smart_neighborhood!')
    chat_id = update['message']['chat']['id']
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Questo bot invia un messaggio ogni volta che il sistema smart_neighborhood apre o chiude gli scuri in modo autonomo.')
    
def send_notification(new_state):
    for chat_id in chat_ids:
        updater.bot.send_message(chat_id=chat_id,
                                 text='Il sistema smart_neighborhood ha deciso che i tuoi scuri verrano %s. \
                                 Se vuoi gestirli manualmente utilizza la web app %s' % (state_dict[new_state], WEB_APP_URL))


def start_bot():
    global updater
    updater = Updater(BOTKEY_TELEGRAM, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    return updater


if __name__ == '__main__':
    updater = start_bot()
    updater.idle()
