from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "YOUR_BOT_TOKEN"

async def handle_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    
