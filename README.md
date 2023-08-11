# djangoProjectSchoolNotifier
School notifier app using mail and telegram. Can generate reports and charts about school information fetched from Kaggle using flask api

This is a django project and requires python3 to run.

To setup this project in local follow the below steps:

1. To install virtual environment **pip install virtualenv**
2. To create virtual env **python3 -m venv poc**
3. To activate virtual env **source poc/bin/activate**
4. To install dependencies **pip install -r requirements.txt**
5. To start the app **python manage.py runserver**

This app requires data to be fetched from Kaggle using a flask api.

This app has a feature to contact openai to use the **text-davinci-003** to generate text/answers based on user input in the Template Generator screen.
To use this you need to replace the openai apikey in **settings.json** file.

To create the key follow the link https://gptforwork.com/help/gpt-for-docs/setup/create-openai-api-key
Now place the generated key in **settings.json** -> **openai** -> **api_key**.
