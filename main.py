import requests
import telegram
import time
import logging

from environs import Env
from logger import TelegramLogHandler


logger = logging.getLogger('Logger')

def main():
    env = Env()
    env.read_env()

    TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
    LONG_POLLING_URL = env('LONG_POLLING_URL')
    AUTHORIZATION_TOKEN = env('AUTHORIZATION_TOKEN')
    TG_CHAT_ID = env('TG_CHAT_ID')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, TG_CHAT_ID))
    logger.info('Бот запущен')
    timestamp = None

    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(f'{LONG_POLLING_URL}',
                                    params=payload,
                                    headers={
                                        'Authorization': f'Token \
                                            {AUTHORIZATION_TOKEN}'
                                        },
                                    timeout=90)

            homeworks = response.json()
            timestamp = homeworks.get('last_attempt_timestamp')

            if response.status_code != 200:
                print(f'status: {response.status_code},\
                      text: {response.text}')

            if homeworks.get('status') == 'found':
                for attempt in homeworks.get('new_attempts'):
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
        except Exception as e:
            logger.exception(e)


if __name__ == '__main__':
    main()
