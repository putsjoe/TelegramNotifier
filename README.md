# TelegramNotifier
A simple API and admin page to send messages to a telegram bot

## Run locally
  `python -m venv env .`
  
  `pip install -r requirements.txt`
  
  `FLASK_APP=app.py flask run --reload`

## Setup
No logging or database, data.py is used to read and write to a file called config.p and any persistence is kept there.
Simply passes on a message to a given telegram bot and specific user, so the telegram bot must be enabled by the given user.


## Environment Variables

ADMIN_URL=/user-admin/ - Changes the admin URL the user uses to change settings.

NOTIFY_URL=/notify/ - The url to send notification API calls to.

USER_NAME, USER_PASS - The username and password to use when logging into the admin url. The default is admin/admin
