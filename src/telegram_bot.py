import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from project.src.ai_agent import workflow
from dotenv import load_dotenv
load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("Please set TELEGRAM_TOKEN environment variable")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm up and running. Send me anything and I'll echo it back.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    answer=workflow.invoke({"question" : text})["answer"]
    await update.message.reply_text(answer)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - start\n/help - help\nOr just message me and I'll echo.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot starting — press Ctrl+C to stop")
    app.run_polling()

if __name__ == "__main__":
    main()
