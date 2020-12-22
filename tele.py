import telebot
import random
import requests
import schedule
import sched, time
import threading
from telebot import types
from pyowm import OWM
from pyowm.utils.config import get_default_config
from bs4 import BeautifulSoup
from multiprocessing.context import Process

config_dict = get_default_config()
config_dict['language'] = 'ru'
bot = telebot.TeleBot("1417359954:AAEWKGylMxCRYftha3N6iLjveM2M8xHHgks")
owm = OWM('c4153a7bc6d29047fcba68583813033b', config_dict)

user1 = 437398899
user2 = 949164017
user3 = 0
user4 = 0
user5 = 0
user6 = 0
user7 = 0
user8 = 0
user9 = 0
user10 = 0



@bot.message_handler(commands=["start"])
def start_message(message):
  user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
  user_markup.row("Погода", "Курсы валют", "Орел/Решка", "Корона", "Прогноз погоды")
  bot.send_message(message.chat.id, "Привет, я - бот, который предоставляет информацию. После ввода комманды /start откроется клавиатура. Нажав на кнопку, ты или выполнишь комманду, или откроешь допольнительные кнопки, нажав на которые получишь информацию.")
  bot.send_message(message.chat.id, "Также, мой автор(а он к слову @ez_ace) предусмотрел авторассылку прогноза погоды рано утром на сегодня. Если заинтересовало - пропиши /mail , и через некоторое время ты будешь получать рассылку с погодой. Приятного пользования :) ", reply_markup=user_markup)

@bot.message_handler(commands=['mail'])
def startJoin(message):
  bot.send_message(user1, message.chat.id)

@bot.message_handler(commands=['special'])
def send_message2(message):
  URL = 'https://sinoptik.ua/погода-киев/10-дней'
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
  full_page = requests.get(URL, headers=headers)
  soup = BeautifulSoup(full_page.content, 'html.parser')
  tmin = soup.findAll("div", {"class": "min"})
  temp_min = tmin[0].text
  orig1 = temp_min
  tp_min = orig1.replace("мин. ", "")
  tmax = soup.findAll("div", {"class": "max"})
  temp_max = tmax[0].text
  orig2 = temp_max
  tp_max = orig2.replace("макс. ", "")
  desc = soup.findAll("div", {"class": "description"})[0]
  description = desc.text
  if description == "ухудшение видимости до 500 м":
    desc = soup.findAll("div", {"class": "description"})[1]
    description = desc.text
  else:
    bot.send_message(user1, "Доброе утро!" + description + " Минимальная температура составит " + tp_min + " , а максимальная " + tp_max)
    bot.send_message(user2, "Доброе утро!" + description + " Минимальная температура составит " + tp_min + " , а максимальная " + tp_max)
#   bot.send_message(user3, "Доброе утро!" + description + " Минимальная температура составит " + tp_min + " , а максимальная " + tp_max)




def send_message1():
  URL = 'https://sinoptik.ua/погода-киев/10-дней'
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
  full_page = requests.get(URL, headers=headers)
  soup = BeautifulSoup(full_page.content, 'html.parser')
  tmin = soup.findAll("div", {"class": "min"})
  temp_min = tmin[0].text
  orig1 = temp_min
  tp_min = orig1.replace("мин. ", "")
  tmax = soup.findAll("div", {"class": "max"})
  temp_max = tmax[0].text
  orig2 = temp_max
  tp_max = orig2.replace("макс. ", "")
  desc = soup.findAll("div", {"class": "description"})[0]
  description = desc.text
  if description == "ухудшение видимости до 500 м":
    desc = soup.findAll("div", {"class": "description"})[1]
    description = desc.text
  else:
    bot.send_message(user1, "Доброе утро!" + description + " Минимальная температура составит " + tp_min + " , а максимальная " + tp_max)
    bot.send_message(user2, "Доброе утро!" + description + " Минимальная температура составит " + tp_min + " , а максимальная " + tp_max)
#   bot.send_message(user3, "Доброе утро!" + description + " Минимальная температура составит " + tp_min + " , а максимальная " + tp_max)

schedule.every().day.at("05:00").do(send_message1)                    #ВРЕМЯЯЯЯЯЯЯ

class ScheduleMessage():
  def try_send_schedule():
    while True:
      schedule.run_pending()
      time.sleep(1)
 
  def start_process():
    p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
    p1.start()

@bot.message_handler(regexp="Прогноз погоды")
def forecast(message):
  keyboardforecast = telebot.types.InlineKeyboardMarkup()
  fc1 = telebot.types.InlineKeyboardButton(text="на сегодня", callback_data="today")
  fc2 = telebot.types.InlineKeyboardButton(text="на завтра", callback_data="tomorrow")
  keyboardforecast.add(fc1, fc2)
  bot.send_message(message.chat.id, "Узнать мин/макс температуру:", reply_markup=keyboardforecast)

@bot.message_handler(regexp="Корона")
def corona(message):
  keyboardCov = telebot.types.InlineKeyboardMarkup()
  cb1 = telebot.types.InlineKeyboardButton(text="за последние 24 часа в Киеве", callback_data="l24")
  cb2 = telebot.types.InlineKeyboardButton(text="за все время в Киеве", callback_data="all1")
  keyboardCov.add(cb1, cb2)
  bot.send_message(message.chat.id, "Узнать количество заболевших: ", reply_markup=keyboardCov)


@bot.message_handler(regexp="Погода")
def selectCounrty(message):
    # Клавиатура выбора стран
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb1 = telebot.types.InlineKeyboardButton(text="Киев", callback_data="country1")
    kb2 = telebot.types.InlineKeyboardButton(text="Москва", callback_data="country2")
    kb3 = telebot.types.InlineKeyboardButton(text="Дубаи", callback_data="country3")
    kb4 = telebot.types.InlineKeyboardButton(text="Шарм-эль-Шейх", callback_data="country4")
    kb5 = telebot.types.InlineKeyboardButton(text="Валенсия", callback_data="country5")
    kb6 = telebot.types.InlineKeyboardButton(text="Брно", callback_data="country6")
    kb7 = telebot.types.InlineKeyboardButton(text="Быдгощ", callback_data="country7")
    keyboard.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7)
    bot.send_message(message.chat.id, "Погода в выбраной стране: ", reply_markup=keyboard)

@bot.message_handler(regexp="Курсы валют")
def value_message(message):
    keyboardV = telebot.types.InlineKeyboardMarkup()
    kbv1 = telebot.types.InlineKeyboardButton(text="Доллар", callback_data="USD")
    kbv2 = telebot.types.InlineKeyboardButton(text="Евро", callback_data="EUR")
    kbv3 = telebot.types.InlineKeyboardButton(text="Польский злотый", callback_data="PLN")
    keyboardV.add(kbv1, kbv2, kbv3)
    bot.send_message(message.chat.id, "Выберите валюту: ", reply_markup=keyboardV)

@bot.callback_query_handler(func=lambda call:True)
def inline(call):
  if call.data == 'country1':
    place = 'Киев'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'country2':
    place = 'Москва'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'country3':
    place = 'Дубай'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'country4':
    place = 'Шарм-эль-Шейх'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'country5':
    place = 'Валенсия'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'country6':
    place = 'Брно'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'country7':
    place = 'Быдгощ'
    try:
      bot.answer_callback_query(callback_query_id=call.id, text='Ищем погоду!')
      mgr = owm.weather_manager()
      observation = mgr.weather_at_place(place)
      w = observation.weather
      weather = mgr.weather_at_place(place).weather
      temp_dict_celsius = weather.temperature('celsius')['temp']
      bot.send_message(call.message.chat.id, 'В городе ' + place + ' сейчас ' + w.detailed_status )
      bot.send_message(call.message.chat.id, "На улице " + str(temp_dict_celsius) + " градусов по Цельсию.")
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      bot.send_message(call.message.chat.id,'Ошибка! Город не найден.')
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'USD':
    bot.answer_callback_query(callback_query_id=call.id, text='Получаем информацию... Пожалуйста, подождите.')
    HRN_USD = 'https://www.google.com/search?client=opera-gx&sxsrf=ALeKk02mV6D-j7a_mb97Q9GyechURetOIg%3A1608241595077&ei=u9HbX8OJBIK73AOJyLvYBA&q=доллар+к+гривне&oq=доллар&gs_lcp=CgZwc3ktYWIQARgAMgkIIxAnEEYQggIyBAgjECcyCAgAEMkDEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLAToICAAQyQMQkQI6BQgAEJECOgIIADoICC4QxwEQowI6BQgAEMkDOgIILjoJCAAQyQMQChAqOgQIABAKOgcIIxDqAhAnOgYIIxAnEBM6CwguEMcBEKMCEMkDOgoIABDJAxAUEIcCUJrNLVii4i1g9OctaAVwAXgAgAGbAYgB9AiSAQM2LjWYAQCgAQGqAQdnd3Mtd2l6sAEKuAECwAEB&sclient=psy-ab'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
    full_page = requests.get(HRN_USD, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", 'data-precision': 2})
    kurs = convert[0].text
    bot.send_message(call.message.chat.id, 'Отношение курса Гривны к Доллару: ' + str(kurs) + ' к 1')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'EUR':
    bot.answer_callback_query(callback_query_id=call.id, text='Получаем информацию... Пожалуйста, подождите.')
    HRN_EUR = 'https://www.google.com/search?client=opera-gx&hs=FDx&sxsrf=ALeKk02bTyXm-nlXNsi5n0l2l2V0eNjwWQ%3A1608213024694&ei=IGLbX9PoKamZlwSFuLbgBQ&q=евро+к+гривне&oq=евро+к+гривне&gs_lcp=CgZwc3ktYWIQAzINCAAQyQMQywEQRhCCAjIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLAToECCMQJzoFCAAQyQM6AggAOggIABDJAxDLAToHCAAQChDLAToKCAAQyQMQChDLAToICAAQFhAKEB46BggAEBYQHlDcEVjzJWCYJ2gCcAF4AIABiwGIAbANkgEEMi4xM5gBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjT-LywlNXtAhWpzIUKHQWcDVwQ4dUDCAw&uact=5'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
    full_page = requests.get(HRN_EUR, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", 'data-precision': 2})
    kurs = convert[0].text
    bot.send_message(call.message.chat.id, 'Отношение курса Гривны к Евро: ' + str(kurs) + ' к 1')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'PLN':
    bot.answer_callback_query(callback_query_id=call.id, text='Получаем информацию... Пожалуйста, подождите.')
    HRN_PLN = 'https://www.google.com/search?client=opera-gx&sxsrf=ALeKk01D4JIpsQsXR_lQv3UK0ilXzKLY7Q%3A1608213393815&ei=kWPbX5yhMY2wrgSpnbXYCQ&q=злотый+к+гривне&oq=злотый+к+гривне&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywE6BAgAEEdQvNMBWIfUAWD52wFoAHACeACAAYkBiAGSApIBAzAuMpgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjcrb7gldXtAhUNmIsKHalODZsQ4dUDCAw&uact=5'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
    full_page = requests.get(HRN_PLN, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", 'data-precision': 2})
    kurs = convert[0].text
    bot.send_message(call.message.chat.id, 'Отношение курса Гривны к Польскому злотому: ' + str(kurs) + ' к 1')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'l24':
    bot.answer_callback_query(callback_query_id=call.id, text='Получаем информацию... Пожалуйста, подождите.')
    TWURL = "https://news.google.com/covid19/map?hl=en-US&mid=%2Fm%2F02h7_7&gl=US&ceid=US%3Aen"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
    full_page = requests.get(TWURL, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    #covid = soup.findAll("div", {"class": "tIUMlb"})
    covid = soup.findAll("strong")
    info = covid[0].text
    original = info
    removed = original.replace("+", "")
    bot.send_message(call.message.chat.id, "За прошлые сутки в Киеве было обнаружено " + removed + " случаев Covid 19")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'all1':
    bot.answer_callback_query(callback_query_id=call.id, text='Получаем информацию... Пожалуйста, подождите.')
    TWURL = "https://www.google.com/search?client=opera-gx&sxsrf=ALeKk03wvz5xvCFcVgOzSW446wtqZW8r4g%3A1608601206348&ei=dk7hX_TSFOrLrgT2m6WACA&q=коронавирус+киев&oq=&gs_lcp=CgZwc3ktYWIQARgAMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnOgcIIxDJAxAnOgQIIxAnOgUIABDLAVDjUFjjUGDRW2gBcAB4AIABWogBWpIBATGYAQCgAQGqAQdnd3Mtd2l6sAEKwAEB&sclient=psy-ab"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
    full_page = requests.get(TWURL, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    covid = soup.findAll("div", {"jsname": "fUyIqc"})            #1111111111111111111
    info = covid[0].text
    original = info
    removed = original.replace("K", "")
    bot.send_message(call.message.chat.id, "За период 2020-го года в городе Киев было обнаружено " + removed + " тысяч случаев Covid 19")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
  if call.data == 'today':
    try:
      URL = 'https://sinoptik.ua/погода-киев/10-дней'
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
      full_page = requests.get(URL, headers=headers)
      soup = BeautifulSoup(full_page.content, 'html.parser')
      tmin = soup.findAll("div", {"class": "min"})
      temp_min = tmin[0].text
      orig1 = temp_min
      tp_min = orig1.replace("мин. ", "")
      tmax = soup.findAll("div", {"class": "max"})
      temp_max = tmax[0].text
      orig2 = temp_max
      tp_max = orig2.replace("макс. ", "")
      desc = soup.findAll("div", {"class": "description"})[0]
      description = desc.text
      if description == "ухудшение видимости до 500 м":
        desc = soup.findAll("div", {"class": "description"})[1]
        description = desc.text
        bot.send_message(call.message.chat.id, "На сегодня минимальная температура составит " + tp_min + " , а минимальная " + tp_max)
        bot.send_message(call.message.chat.id, description)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
      else:
        bot.send_message(call.message.chat.id, "На сегодня минимальная температура составит " + tp_min + " , а минимальная " + tp_max)
        bot.send_message(call.message.chat.id, description)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      pass
  if call.data == 'tomorrow':
    try:
      RURL = 'https://sinoptik.ua/погода-киев/10-дней'
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456'}
      full_page = requests.get(RURL, headers=headers)
      soup = BeautifulSoup(full_page.content, 'html.parser')
      tmin = soup.findAll("div", {"class": "min"})
      temp_min = tmin[1].text
      orig1 = temp_min
      tp_min = orig1.replace("мин. ", "")
      tmax = soup.findAll("div", {"class": "max"})
      temp_max = tmax[1].text
      orig2 = temp_max
      tp_max = orig2.replace("макс. ", "")
      bot.send_message(call.message.chat.id, "На завтра минимальная температура составит " + tp_min + " , а минимальная " + tp_max)
      bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
      pass

@bot.message_handler(regexp="Орел/Решка")
def coinflip(message):
  x = random.randint(0, 100)
  if x % 2 == 0:
    bot.send_message(message.chat.id, "Орел" )
  else:
    bot.send_message(message.chat.id, "Решка" )

if __name__ == '__main__':
  ScheduleMessage.start_process()
  try:
    bot.polling(none_stop=True)
  except:
    pass



  
  
