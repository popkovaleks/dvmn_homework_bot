import requests
import telegram

from environs import Env

env = Env()

env.read_env()


TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
LONG_POLLING_URL = env('LONG_POLLING_URL')
AUTHORIZATION_TOKEN = env('AUTHORIZATION_TOKEN')
CHAT_ID = env('CHAT_ID')


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = None
    while True:
        try:
            response = requests.get(f'{LONG_POLLING_URL}/?timestamp={timestamp}' if timestamp else LONG_POLLING_URL, headers={'Authorization': f'Token {AUTHORIZATION_TOKEN}'}, timeout=90)
            print(response.json().get('status'))
            timestamp = response.json().get('last_attempt_timestamp')
            print(timestamp)
            if response.json().get('status') == 'found':
                bot.send_message(text='Преподаватель проверил работу!', chat_id=CHAT_ID)
        except requests.exceptions.ReadTimeout:
            print("Timeout occured")
        except requests.exceptions.ConnectionError:
            print("No internet connection")


if __name__ == '__main__':
    main()