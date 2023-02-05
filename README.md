# whisper-telegram-bot
Telegram bot for transcriptions of audio files using Whisper for CPU


## Usage

Firstly, clone the repo and install the module of the OpenAI Whisper repo with the
modifications needed for CPU dynamic quantization:

```bash
git clone https://github.com/costiash/whisper-telegram-bot.git
pip install -e ./whisper
```

## Creating telegram bot

To create a chatbot on Telegram, you need to contact the BotFather, which is essentially a bot used to create other bots.
The command you need is /newbot which leads to the following steps to create your bot:

![telb](https://user-images.githubusercontent.com/63783894/216820639-7cb189f0-c1b9-43bf-930f-3d242a381c33.jpg)

Your bot should have two attributes: a name and a username. The name will show up for your bot, while the username will be used for mentions and sharing.
After choosing your bot name and username—which must end with “bot”—you will get a message containing your access token, and you’ll obviously need to save your access token and username for later, as you will be needing them.

<b>Your access token is your API key, it's what connect between the logic of your bot to the actual telegram bot.</b>

## Local Usage

For local usage just run:

```bash
python main.py
```

and then go to your bot via the link you recived when creating it.


## Deployment to Google Cloud Run
The Docker file is already in the repo and is customized for deployment of the bot, just make sure to comment/uncomment the relevant lines in the main.py file.

1. Setup Google Cloud
   - Create new project
   - Activate Cloud Run API and Cloud Build API
 
2. Install and init Google Cloud SDK
   - https://cloud.google.com/sdk/docs/install

3. Cloud build & deploy
```bash
export TOKEN=<your_token_api>
gcloud builds submit --tag gcr.io/<project_id>/index
gcloud run deploy bot --image gcr.io/<project_id>/index --cpu 4 --memory 16Gi --platform managed --set-env-vars TOKEN=${TOKEN}
```

4. Creating the webhook between the Cloud Run endpoint and the telegram bot
```bash
curl "https://api.telegram.org/bot${TOKEN}/setWebhook?url=$(gcloud run services describe bot --format 'value(status.url)' --project <project_id>)"
```

Link to a youtube video that demonstrate the deployment steps:
https://www.youtube.com/watch?v=vieoHqt7pxo

## References
1. https://github.com/MiscellaneousStuff/openai-whisper-cpu
2. https://github.com/python-telegram-bot/python-telegram-bot
