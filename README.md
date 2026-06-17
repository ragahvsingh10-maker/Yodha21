from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "YOUR_BOT_TOKEN"

async def handle_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if document.file_name.endswith(".txt"):
        file = await document.get_file()
        await file.download_to_drive("data.txt")

        with open("data.txt", "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) > 4000:
            content = content[:4000]

        await update.message.reply_text(content)

        with open("data.txt", "rb") as f:
            await update.message.reply_document(f)
