from telegram import Update
from telegram.ext import CallbackContext
import datetime
import db

class Sade:
    def __init__(self):
        self.commands = {'purge': self.doPurge}

    def getCommands(self):
        return self.commands

    # Purge everyone who has been idle for more than 69 days
    def doPurge(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        saasta = db.findSaasta(chat_id)
        duration = datetime.datetime.now() + datetime.timedelta(minutes=1)

        for lurker in saasta:
            context.bot.kickChatMember(chat_id, lurker[0], until_date=duration)

    # Rip DB
    def setLastSeen(self, update: Update):
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        db.updateLastSeen(user_id, chat_id)

    def messageHandler(self, update: Update, context: CallbackContext):

        ### Need to add logic here where we set last seen for a joining user
        ### Otherwise someone who joined can lurk and never get purged

        msg = update.message
        if msg.text is not None:
            # Only the chosen one can do the purge
            if 'purge' in msg.text.lower() and (update.message.from_user.id == 107460801):
                self.doPurge(update, context)
                self.setLastSeen(update)
            else:
                self.setLastSeen(update)