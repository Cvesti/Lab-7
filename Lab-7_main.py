import requests
from datetime import datetime

def get_weather(api_key, city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        
        main_info = weather_data['main']
        weather_info = weather_data['weather'][0]
        wind_info = weather_data['wind']
        sys_info = weather_data['sys']
        
        # Форматирование данных
        result = {
            "Город": weather_data['name'],
            "Текущая температура": f"{main_info['temp']}°C",
            "Ощущается как": f"{main_info['feels_like']}°C",
            "Погодные условия": weather_info['description'].capitalize(),
            "Влажность": f"{main_info['humidity']}%",
            "Атмосферное давление": f"{main_info['pressure']} гПа",
            "Скорость ветра": f"{wind_info['speed']} м/с",
            "Восход солнца": format_time(sys_info['sunrise']),
            "Закат солнца": format_time(sys_info['sunset']),
            "Облачность": f"{weather_data['clouds']['all']}%"
        }
        
        return result
    
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к API: {e}"
    except KeyError as e:
        return f"Ошибка при обработке данных: отсутствует ключ {e}"

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M')

if __name__ == "__main__":
    API_KEY = 'a2cb2fad32bf8bb4cd234fd3d06b5bdd'
    CITY_NAME = 'Санкт-Петербург'
    
    weather_info = get_weather(API_KEY, CITY_NAME)
    
    if isinstance(weather_info, dict):
        print(f"\nПогода в городе {CITY_NAME}:")
        print("=" * 40)
        for key, value in weather_info.items():
            print(f"{key:25}: {value}")
        print("=" * 40)
    else:
        print(weather_info)