import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import schedule
import time
import telebot
import re
import calendar

TOKEN = '6927115520:AAHuPb90D12VyV0czqWxhMlnmCyUZ6rV0I0'
CHANNEL_ID = '@horoscope_post'
TARO_BOT_USERNAME = '@RaskladTaroOnline_bot'
bot = telebot.TeleBot(TOKEN)

signs = {
    '   Гороскоп для всех знаков зодиака:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/',
                                   'selector': 'div.sign__description-text'},
    '♈ Гороскоп для знака Овен:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/aries/',
                                   'selector': 'div.sign__description-text'},
    '♉ Гороскоп для знака Телец:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/taurus/',
                                    'selector': 'div.sign__description-text'},
    '♊ Гороскоп для знака Близнецы:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/gemini/',
                                       'selector': 'div.sign__description-text'},
    '♋ Гороскоп для знака Рак:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/cancer/',
                                    'selector': 'div.sign__description-text'},
    '♌ Гороскоп для знака Лев:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/leo/',
                                    'selector': 'div.sign__description-text'},
    '♍ Гороскоп для знака Дева:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/virgo/',
                                    'selector': 'div.sign__description-text'},
    '♎ Гороскоп для знака Весы:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/libra/',
                                    'selector': 'div.sign__description-text'},
    '♏ Гороскоп для знака Скорпион:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/scorpio/',
                                    'selector': 'div.sign__description-text'},
    '♐ Гороскоп для знака Стрелец:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/sagittarius/',
                                    'selector': 'div.sign__description-text'},
    '♑ Гороскоп для знака Козерог:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/capricorn/',
                                    'selector': 'div.sign__description-text'},
    '♒ Гороскоп для знака Водолей:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/aquarius/',
                                    'selector': 'div.sign__description-text'},
    '♓ Гороскоп для знака Рыбы:': {'url': 'https://www.thevoicemag.ru/horoscope/daily/pisces/',
                                    'selector': 'div.sign__description-text'},
}

weekly_signs = {
    '♈ Гороскоп для знака Овен на #неделю:': {'url': 'https://horo.mail.ru/prediction/aries/week/',
                                           'selector': '.article_prediction'},
    '♉ Гороскоп для знака Телец на #неделю:': {'url': 'https://horo.mail.ru/prediction/taurus/week/',
                                    'selector': '.article_prediction'},
    '♊ Гороскоп для знака Близнецы на #неделю:': {'url': 'https://horo.mail.ru/prediction/gemini/week/',
                                       'selector': '.article_prediction'},
    '♋ Гороскоп для знака Рак на #неделю:': {'url': 'https://horo.mail.ru/prediction/cancer/week/',
                                    'selector': '.article_prediction'},
    '♌ Гороскоп для знака Лев на #неделю:': {'url': 'https://horo.mail.ru/prediction/leo/week/',
                                    'selector': '.article_prediction'},
    '♍ Гороскоп для знака Дева на #неделю:': {'url': 'https://horo.mail.ru/prediction/virgo/week/',
                                    'selector': '.article_prediction'},
    '♎ Гороскоп для знака Весы на #неделю:': {'url': 'https://horo.mail.ru/prediction/libra/week/',
                                    'selector': '.article_prediction'},
    '♏ Гороскоп для знака Скорпион на #неделю:': {'url': 'https://horo.mail.ru/prediction/scorpio/week/',
                                    'selector': '.article_prediction'},
    '♐ Гороскоп для знака Стрелец на #неделю:': {'url': 'https://horo.mail.ru/prediction/sagittarius/week/',
                                    'selector': '.article_prediction'},
    '♑ Гороскоп для знака Козерог на #неделю:': {'url': 'https://horo.mail.ru/prediction/capricorn/week/',
                                    'selector': '.article_prediction'},
    '♒ Гороскоп для знака Водолей на #неделю:': {'url': 'https://horo.mail.ru/prediction/aquarius/week/',
                                    'selector': '.article_prediction'},
    '♓ Гороскоп для знака Рыбы на #неделю:': {'url': 'https://horo.mail.ru/prediction/pisces/week/',
                                    'selector': '.article_prediction'},
}

previous_horoscopes = {url: '' for url in [data['url'] for data in signs.values()]}
def get_horoscope_for_sign(url, selector, paragraph_index=0):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.select(selector)
    if paragraphs:
        if paragraph_index < len(paragraphs):
            return paragraphs[paragraph_index].text.strip()
    return "Гороскоп не найден"
def parse_horoscope(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        horoscope = soup.select(selector)[0].text
        return horoscope
    except (IndexError, requests.exceptions.RequestException) as e:
        return "Гороскоп не найден"


def get_month_name(month_num):
    months_russian = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
    return months_russian[month_num - 1]


def get_moon_phase_info(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    moon_phase_info = soup.select(selector)

    if moon_phase_info:
        text = moon_phase_info[0].text.strip()
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        filtered_sentences = sentences[1:]  # Выбираем все предложения, начиная со второго
        return ' '.join(filtered_sentences)

    return "Информация о фазе луны не найдена"


def send_moon_phase_info():
    moon_url = "https://mirkosmosa.ru/lunar-calendar/phase-moon/lunar-day-today"
    moon_selector = ".div_table:nth-of-type(4)"
    moon_info = get_moon_phase_info(moon_url, moon_selector)
    today = datetime.now()
    day_selector = "h3:-soup-contains('лунный день')"
    day_response = requests.get(moon_url)
    day_soup = BeautifulSoup(day_response.text, 'html.parser')
    lunar_day = day_soup.select(day_selector)[0].text
    month_name = get_month_name(today.month)
    formatted_date = f"{today.day} {month_name.lower().capitalize()}"
    message_text = f'<u>Информация о фазе луны🌜:</u>\n<code>{formatted_date} - {lunar_day}</code>\n\n<span class="tg-spoiler"><i>{moon_info}</i></span>\n\nБесплатный бот по раскладу Таро: {TARO_BOT_USERNAME}'
    send_to_telegram_channel(message_text)


def get_moon_sign_info(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    moon_sign_info = soup.select(selector)

    if moon_sign_info:
        text = moon_sign_info[0].text.strip()
        return text

    return "Информация о знаке Луны не найдена"


def send_moon_sign_info():
    moon_sign_url = "https://mirkosmosa.ru/lunar-calendar/phase-moon/lunar-day-today"
    moon_sign_selector = ".moon_desc_plus"
    moon_info = get_moon_sign_info(moon_sign_url, moon_sign_selector)
    message_text = f"🌙 <u>Информация о знаке Луны на сегодня:</u> 🌙\n\n<i>{moon_info}</i>\n\nБесплатный бот по раскладу Таро: {TARO_BOT_USERNAME}"
    send_to_telegram_channel(message_text)

def get_day_of_week_info(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    day_of_week_info = soup.select(selector)

    if day_of_week_info:
        text = day_of_week_info[0].text.strip()
        return text

    return "Информация о дне недели не найдена"

def send_day_of_week_info():
    day_of_week_url = "https://mirkosmosa.ru/lunar-calendar/phase-moon/lunar-day-today"
    day_of_week_selector = "h3:-soup-contains('Влияние дня недели (±)') + .moon_desc_normal"
    day_of_week_info = get_day_of_week_info(day_of_week_url, day_of_week_selector)
    message_text = f"🌟 <u>Влиянии дня недели:</u> 🌟\n\n<i>{day_of_week_info}</i>\n\nБесплатный бот по раскладу Таро: {TARO_BOT_USERNAME}"
    send_to_telegram_channel(message_text)
def send_to_telegram_channel(message):
    bot.send_message(CHANNEL_ID, message, parse_mode='HTML')

def send_weekly_horoscopes():
    for sign, data in weekly_signs.items():
        horoscope = parse_horoscope(data['url'], data['selector'])
        start_date = datetime.today().strftime('%d')
        end_date = (datetime.today() + timedelta(days=7)).strftime('%d.%m')
        message_text = f'<b>{sign} (с  по 17.03):</b>\n{horoscope}\n\nБесплатный бот по раскладу Таро: {TARO_BOT_USERNAME}'
        send_to_telegram_channel(message_text)

def send_horoscopes():
    for sign, data in signs.items():
        if '(#неделя)' not in sign:
            horoscope = get_horoscope_for_sign(data['url'], data['selector'])
            today_date = datetime.today().strftime('%d.%m.%Y')
            message_text = f"<b>{sign} {today_date}:</b>\n{horoscope}\n\nБесплатный бот по раскладу Таро: {TARO_BOT_USERNAME}"
            bot.send_message(CHANNEL_ID, message_text, parse_mode='HTML')
            previous_horoscopes[data['url']] = horoscope

schedule.every().friday.at("17:23").do(send_weekly_horoscopes)
schedule.every().day.at('05:00').do(send_horoscopes)
schedule.every().day.at('10:36').do(send_moon_phase_info)
schedule.every().day.at('10:34').do(send_moon_sign_info)
schedule.every().day.at('10:35').do(send_day_of_week_info)
while True:
    schedule.run_pending()
    time.sleep(1)

bot.polling()