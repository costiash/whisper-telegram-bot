# WhisperMe-telegram-bot
Telegram bot for transcriptions of audio files using Whisper for CPU


## Usage

Firstly, clone the repo and install the module of the OpenAI Whisper repo with the
modifications needed for CPU dynamic quantization:

```bash
git clone https://github.com/costiash/WhisperMe-telegram-bot.git
pip install -e ./whisper
```

### Creating telegram bot

To create a chatbot on Telegram, you need to contact the BotFather, which is essentially a bot used to create other bots.
The command you need is /newbot which leads to the following steps to create your bot:
[image]

Your bot should have two attributes: a name and a username. The name will show up for your bot, while the username will be used for mentions and sharing.
After choosing your bot name and username—which must end with “bot”—you will get a message containing your access token, and you’ll obviously need to save your access token and username for later, as you will be needing them.

[b]Your access token is your API key, it's what connect between the logic of your bot to the actual telegram bot.

### Local Usage

For local usage just run:

```bash
python main.py
```

and then go to your bot via the link you recived when creating it.


### Deployment to Google Cloud Run

will be updated soon