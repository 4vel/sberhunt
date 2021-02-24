import requests
from data.config import BOT_TOKEN, admins


def send_message(chat_id, token, text='bla-bla-bla'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json = payload)
    return r


if __name__ == "__main__":
    send_message(admins[0], BOT_TOKEN)
