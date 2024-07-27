from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN: Final = "7490927537:AAE9WLIFxu1TFhsT5FwihWInnM2oPfyTnoA"
BOT_USERNAME: Final = "@FostereumBot"

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_textcc(f"""
Hello! I am Reeum, your Fostereum assistant.
I will be assisting you if you need any help, though I am just a simple bot for now. I'll try my best! :D
Here your chat id: {update.message.chat_id}
You can use the chat id I gave you to get weekly report and get alert when plant's environment is not suitable.

For more information, please use /help command.
""")
    
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
I'm here to help you with your Fostereum needs! Here are some useful commands:
- /start  : to start using my functions
- /help   : to get this help message
- /chatid : to get your chat id
                                    
You can toggle your option to get weekly report and get alert from the web.""")

async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Here's your weekly report:
""")
async def chatid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Don't worry! I gotcha.\nHere's your chat id : {update.message.chat_id}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error '{context.error}'")
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_cmd))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(CommandHandler('chatid', chatid_cmd))
    app.add_error_handler(error)
    print("Polling..")
    app.run_polling(poll_interval=5)