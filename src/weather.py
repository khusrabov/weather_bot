# Importing required modules
import datetime
import requests

from src.config import WEATHER_API_KEY
from src.GLOBAL import emojy

Current_City = ''


# function for parsing the current weather in the 'city' from OpenWeatherMap API
def parse_openweather(city):
    # current weather-URL
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'

    # Sending a request get to the URL
    response = requests.get(URL)
    # response.status_code returns a number that indicates the status (200 is OK)
    if response.status_code == 200:
        # Extracting the contents of the request URL
        data = response.json()
        return data
    else:
        return 0


# function for parsing the weather forecast (5 days) from OpenWeatherMap API
def parse_openweather_forecast(city):
    # forecast-URL
    URL = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric'

    # Sending a request get to the URL
    response = requests.get(URL)
    # response.status_code returns a number that indicates the status (200 is OK)
    if response.status_code == 200:
        # Extracting the contents of the request URL
        data = response.json()
        return data
    else:
        return 0


# the main function for getting the state of the weather in the city
def get_weather(city):
    # getting the data
    data = parse_openweather(city)
    if data == 0:
        return 0

    # We leave the data about the name of the current city
    global Current_City
    Current_City = data['name']

    # We get the coordinates of the city
    lat = data['coord']['lat']
    lon = data['coord']['lon']

    # sending a request for time zone data
    timezone_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    if timezone_url == 0:
        return 0
    timezone_data = requests.get(timezone_url).json()

    # get the time zone offset relative to UTC in seconds
    timezone_offset = timezone_data['timezone']

    # get the current date and time in the specified city
    local_time = datetime.datetime.utcfromtimestamp(data['dt'] + timezone_offset)

    # formatting the date and time for output
    local_time = local_time.strftime('%d.%m.%Y %H:%M:%S')
    weather_description = data['weather'][0]['main']
    if weather_description in emojy:
        weather_description = emojy[weather_description]
    else:
        pass
    weather = data['main']['temp']
    # return data
    return (
        f"Погода в городе {city.title()} {weather}ºC\n"
        f"Сегодня: {weather_description}\n"
        f'Дата и время: {local_time} {emojy["time"]}'
    )


# the function that returns detailed information about the weather in the current city
def weather_more():
    # Getting the current city for further data parsing
    global Current_City
    data = parse_openweather(Current_City)

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    teap_max = data["main"]["temp_max"]
    teap_min = data["main"]["temp_min"]
    wind_speed = data["wind"]["speed"]

    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
    # return additional information about the weather
    return (
        f'{emojy["telescope"]}Дополнительная информация:\n\n'
        f'Влажность - {humidity}%{emojy["drop"]}\n\n'
        f'Давление - {pressure} {emojy["bomb"]}\n\n'
        f'Минимальная температура - {teap_min}ºC {emojy["min"]}\n\n'
        f'Максимальная температура - {teap_max}ºC {emojy["max"]}\n\n'
        f'Скорость ветра - {wind_speed} {emojy["wind"]}\n\n'
        f'Рассвет - {sunrise} {emojy["sunrise"]}\n\n'
        f'Закат - {sunset} {emojy["sunset"]}'
    )


# function for getting the weather for five days
def weather_week():
    # Getting the current city for further data parsing
    global Current_City
    data = parse_openweather_forecast(Current_City)

    weather_for_week = []
    for item in data['list']:
        date_time_str = item['dt_txt']
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

        if date_time_obj.hour == 12:
            date_str = date_time_obj.strftime('%Y-%m-%d')
            weather_description = item['weather'][0]['main']

            if weather_description in emojy:
                weather_description = emojy[weather_description]
            temp = item['main']['temp']

            if temp >= 20:
                temp_emojy = emojy['hot']
            elif 0 <= temp < 20:
                temp_emojy = emojy['normal']
            else:
                temp_emojy = emojy['cold']

            weather_for_week.append(
                f'{emojy["clock"]}{date_str} - {weather_description},'
                f'Температура: {temp}°C {temp_emojy}'
            )

    return f'\n' '\n'.join(weather_for_week)


# additional function for help output
def helper():
    return (
        f'{emojy["Hand"]}\nЯ бот, который подскажет, как краткую так и '
        f'полную информацию об погоде в любом городе мира!{emojy["Sun_smile"]}\n'
        f'Просто напиши {emojy["write"]} название города.\n'
        f'Я смогу определить название города, как на русском {emojy["Russia"]}, так и на английском{emojy["USA"]}!'
    )


# additional function for error output
def error(city):
    return (
        f'Извините, не удалось получить информацию о погоде в городе: {city.title()},'
        f'проверьте, что вы написали название города правильно.'
    )
