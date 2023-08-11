# djangoProjectSchoolNotifier
School notifier app using mail and telegram. Can generate reports and charts about school information fetched from Kaggle using flask api

This is a django project and requires python3 to run.

To setup this project in local follow the below steps:

1. To install virtual environment **pip install virtualenv**
2. To create virtual env **python3 -m venv poc**
3. To activate virtual env **source poc/bin/activate**
4. To install dependencies **pip install -r requirements.txt**
5. To start the app **python manage.py runserver**

This app requires data to be fetched from Kaggle using a flask api. Replace the data with your own api data in **Home views** and **Reporting views** and change the graphs accordingly.

This app has a feature to contact openai to use the **text-davinci-003** to generate text/answers based on user input in the Template Generator screen.
To use this you need to replace the openai apikey in **settings.json** file.

To create the key follow the link https://gptforwork.com/help/gpt-for-docs/setup/create-openai-api-key
Now place the generated key in **settings.json** -> **openai** -> **api_key**.

This app also contains a functionality to send messages to telegram channel. To send it to your own channel follow the below steps.
1. Create a bot in Telegram using BotFather follow the isntructions from https://help.nethunt.com/en/articles/6253243-how-to-make-an-api-call-to-the-telegram-channel
2. Create a new channel and add the bot to it and make it as admin.
3. Open a channel chat in pc using https://web.telegram.org
4. Look at the URL at the top of the screen. The digits behind the letter “g” are actually your chat ID. Just add “-“ in front of the numbers.
5. Replace your **apiToken** and **chatID** in **settings.json** under the **telegram** key.

