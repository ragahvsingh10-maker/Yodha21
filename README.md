from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8823361453:AAFR7CfpKHtC1UDOMSaDGJMRnl6ISLORRsY"

async def handle_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    
