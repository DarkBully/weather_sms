import os

import dotenv
from twilio.rest import Client

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

dotenv.load_dotenv()


config_dict = get_default_config()
config_dict['language'] = 'ru'
place = 'Moscow'
country = 'Russia'
country_and_place = 'Moscow, Russia'

owm = OWM('790a49443e080242dec5db92895becb4')
mrg = owm.weather_manager()
observation = mrg.weather_at_place(country_and_place)
w = observation.weather

status = w.detailed_status
w.wind()
humidity = w.humidity
temp = w.temperature('celsius')['temp']


def message(text='weath', im='ph_num'):
    try:
        account_sid = os.getenv('SID')
        auth_tocken = os.getenv('TOCKEN')
        client = Client(account_sid, auth_tocken)
        message = client.messages.create(body=text,
                                         from_='12543235824',
                                         to=im)
    except Exception as e:
        print(e, 'Похоже произошла ошибка.')

def send():
    mess = message(text=(f'В городе {place} сейчас {status}.\n Температура {temp} градусов по Цельсию.\n Влажность воздуха составляет {humidity}%.\n Скорость ветра достигает{w.wind()["speed"]} м/с\n'),im=os.getenv('MY_PH_NUM'))
    print(mess)



if __name__ == '__main__':
    send()
