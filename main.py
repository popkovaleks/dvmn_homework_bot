import requests
import telegram
import time

from environs import Env


def main():
    env = Env()
    env.read_env()

    TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
    LONG_POLLING_URL = env('LONG_POLLING_URL')
    AUTHORIZATION_TOKEN = env('AUTHORIZATION_TOKEN')
    TG_CHAT_ID = env('TG_CHAT_ID')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = None

    while True:
        try:
            payload = {'timestamp': timestamp}
            resp_orig = requests.get(f'{LONG_POLLING_URL}',
                                     params=payload,
                                     headers={
                                        'Authorization': f'Token \
                                            {AUTHORIZATION_TOKEN}'
                                        },
                                     timeout=90)

            response = resp_orig.json()
            timestamp = response.get('last_attempt_timestamp')

            if resp_orig.status_code != 200:
                print(f'status: {resp_orig.status_code},\
                      text: {resp_orig.text}')

            if response.get('status') == 'found':
                for attempt in response.get('new_attempts'):
                    mistake = 'Есть замечания!' if attempt.get('is_negative') \
                        else ''
                    message = f'''Преподаватель проверил работу \
                        {attempt.get('lesson_title')}!
                    {mistake}
                    Ссылка на задание: {attempt.get('lesson_url')}'''

                    bot.send_message(text=message, chat_id=TG_CHAT_ID)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(600)


if __name__ == '__main__':
    main()
