import requests
import telegram


TOKEN = '5603108098:AAGJSV_bru0eWqkAxyRMvHIOdg4vK7FzD2o'
URL = 'https://dvmn.org/api/user_reviews/'
LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
AUTHORIZATION_TOKEN = 'b913929505c6e63108a81e9050cc0084c45fd858'

bot = telegram.Bot(token=TOKEN)
timestamp = None
while True:
    try:
        response = requests.get(f'{LONG_POLLING_URL}/?timestamp={timestamp}' if timestamp else LONG_POLLING_URL, headers={'Authorization': f'Token {AUTHORIZATION_TOKEN}'}, timeout=90)
        print(response.json().get('status'))
        timestamp = response.json().get('last_attempt_timestamp')
        print(timestamp)
        if response.json().get('status') == 'found':
            bot.send_message(text='Преподаватель проверил работу!', chat_id=164255835)
    except requests.exceptions.ReadTimeout:
        print("Timeout occured")
    except requests.exceptions.ConnectionError:
        print("No internet connection")