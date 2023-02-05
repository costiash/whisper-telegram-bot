import logging
import os
import http
from queue import Queue
from flask import Flask, request
from werkzeug.wrappers import Response
import warnings
import whisper
import torch
from telegram import Bot, Update
from telegram.ext import Filters, MessageHandler, CallbackContext, CommandHandler, Updater
warnings.filterwarnings("ignore")

MODEL_NAME = '' # Fill in the relevant name of the whisper model you wish to use
DUMMY_AUDIO = '' # Fill in the name to a dummy audio file that is used to initialize the model when the bot start. put rhe audio in the current directory

# Uncomment this linne in case of deployment
# app = Flask(__name__)

# For deployment, make sure to place the model's weights in the current directory
model_fp32 = whisper.load_model(name=MODEL_NAME, device="cpu")
quantized_model = torch.quantization.quantize_dynamic(model_fp32, {torch.nn.Linear}, dtype=torch.qint8)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def predict(audio_file):
    # logging.info("Start Transcribtion!")
    result = whisper.transcribe(quantized_model, audio_file)
    return result["text"]


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    dummy_res = predict(DUMMY_AUDIO)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! I am a multilingual transcription bot powered by the OpenAI Whisper model\. My goal is to assist you in your silent battle with recorded messages\. If you receive a recorded message \(here, on Telegram, or on WhatsApp\), simply forward it to me and I will do my best to provide you with a written transcription\. Just bear in mind that, while I do my best to provide you with an accurate transcription as much as possible, I do make mistakes now and then\.\.\. after all, I am \(not\) only human ;\)\. Simply send an audio file to use my services\.',
    )


# For Voice masseges
def get_voice(update: Update, context: CallbackContext) -> None:
    # get basic info about the voice note file and prepare it for downloading
    new_file = context.bot.get_file(update.message.voice.file_id)
    update.message.reply_text(f"*Got your file! starting to work on the transcription (it might take some time)*", parse_mode='Markdown')
    # download the voice note as a file
    new_file.download(f"voice_note_{update.effective_user}.ogg")
    res = predict(f"voice_note_{update.effective_user}.ogg")
    os.remove(f"voice_note_{update.effective_user}.ogg")
    update.message.reply_text(str(res))


# For Audio files
def get_audio(update: Update, context: CallbackContext) -> None:
    # get basic info about the voice note file and prepare it for downloading
    new_file = context.bot.get_file(update.message.audio.file_id)
    update.message.reply_text(f"*Got your file! starting to work on the transcription (it might take some time)*", parse_mode='Markdown')
    # download the voice note as a file
    new_file.download(f"voice_note_{update.effective_user}.ogg")
    res = predict(f"voice_note_{update.effective_user}.ogg")
    os.remove(f"voice_note_{update.effective_user}.ogg")
    update.message.reply_text(str(res))


def not_valid(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"*Sorry! seems like you didn't send any audio file in your message. I work only with audio files for now.*", parse_mode='Markdown')


# Uncomment these lines in case of deployment
# @app.post("/")
# def index() -> Response:
#     bot = Bot(token=os.environ["TOKEN"])
#     q = Queue()
#     dispatcher = Dispatcher(bot=bot, update_queue=q)
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(MessageHandler(Filters.voice, get_voice))
#     dispatcher.add_handler(MessageHandler(Filters.audio, get_audio))
#     dispatcher.add_handler(MessageHandler(~Filters.audio & ~Filters.voice, not_valid))
#     dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))
    
#     return "", http.HTTPStatus.OK


# Comment all the lines till the end in case of deployment
def main():
    """Start the bot."""
    
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR API KEY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # Add handler for voice messages
    updater.dispatcher.add_handler(MessageHandler(Filters.voice, get_voice))
    updater.dispatcher.add_handler(MessageHandler(Filters.audio, get_audio))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()