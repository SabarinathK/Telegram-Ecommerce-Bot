import os
import tempfile
import asyncio
import threading
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from groq import Groq
from asgiref.sync import sync_to_async
from workflow.graph import workflow
from dotenv import load_dotenv

load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_CLIENT = Groq(api_key=os.environ.get("GROQ_API_KEY")) if TOKEN else None

# Sync functions
def stt_transcribe_sync(file_path: str) -> str:
    with open(file_path, "rb") as file:
        transcription = GROQ_CLIENT.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            language="en",
            temperature=0.0
        )
    return transcription.text


def tts_synthesize_sync(text: str) -> bytes:
    response = GROQ_CLIENT.audio.speech.create(
        model="playai-tts",
        voice="Arista-PlayAI",
        input=text,
        response_format="wav"
    )
    if hasattr(response, "read"):
        return response.read()
    elif hasattr(response, "data"):
        return response.data
    elif isinstance(response, bytes):
        return response
    else:
        raise ValueError(f"Groq TTS returned unexpected type: {type(response)}")


def get_workflow_answer_sync(text: str) -> str:
    return workflow.invoke({"question": text})["answer"]


# Async Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! welcome to Highlet")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - start\n/help - help\n")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    answer = await sync_to_async(get_workflow_answer_sync)(text)
    await update.message.reply_text(answer)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not GROQ_CLIENT:
        await update.message.reply_text("Audio processing disabled (Missing API key).")
        return

    voice = update.message.voice or update.message.audio
    if not voice:
        await update.message.reply_text("Please send a valid voice note.")
        return

    try:
        tg_file = await context.bot.get_file(voice.file_id)
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as ogg_file:
            await tg_file.download_to_drive(ogg_file.name)
            ogg_path = ogg_file.name

        transcription = await sync_to_async(stt_transcribe_sync)(ogg_path)
        answer = await sync_to_async(get_workflow_answer_sync)(transcription)

        tts_response = await sync_to_async(tts_synthesize_sync)(answer)
        tts_path = ogg_path.replace(".ogg", "_reply.wav")
        with open(tts_path, "wb") as f:
            f.write(tts_response)

        await update.message.reply_voice(voice=open(tts_path, "rb"))

    except Exception as e:
        await update.message.reply_text(f"An error occurred during voice processing: {e}")

    finally:
        try:
            if os.path.exists(ogg_path):
                os.remove(ogg_path)
            if os.path.exists(tts_path):
                os.remove(tts_path)
        except Exception:
            pass


if not TOKEN:
    print("⚠️ Missing TELEGRAM_TOKEN, bot not started.")

application = (
    ApplicationBuilder()
    .token(TOKEN)
    .concurrent_updates(False)
    .build()
)

# Register handlers BEFORE initializing
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))


# Setup background event loop and run bot initialization
loop = asyncio.new_event_loop()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


threading.Thread(target=start_loop, args=(loop,), daemon=True).start()


async def _init_bot():
    await application.initialize()
    await application.start()
    print("✅ Telegram bot initialized (Django webhook mode)")
