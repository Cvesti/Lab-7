import requests
import json
from datetime import datetime

def get_news(api_key, city_name, page_size=5):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': city_name,
        'apiKey': api_key,
        'pageSize': page_size,
        'language': 'ru',
        'sortBy': 'publishedAt'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        news_data = response.json()
        
        if news_data['status'] != 'ok':
            return f"Ошибка API: {news_data.get('message', 'Неизвестная ошибка')}"
        
        articles = []
        for article in news_data['articles']:
            article_info = {
                "Источник": article['source']['name'],
                "Автор": article.get('author', 'Не указан'),
                "Заголовок": article['title'],
                "Описание": article['description'],
                "Дата публикации": format_date(article['publishedAt']),
                "URL": article['url'],
            }
            articles.append(article_info)
        
        return articles
    
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к API: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Ошибка при обработке данных: {e}"

def format_date(date_string):
    try:
        dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('%d.%m.%Y %H:%M')
    except:
        return date_string

if __name__ == "__main__":
    NEWS_API_KEY = '5b6d23d4f3f143fd9808f2582e0f90ab'
    CITY_NAME = 'Санкт-Петербург'
    
    news_info = get_news(NEWS_API_KEY, CITY_NAME)
    
    if isinstance(news_info, list):
        print(f"\nПоследние новости о городе {CITY_NAME}:")
        print("=" * 80)
        for i, article in enumerate(news_info, 1):
            print(f"\nНовость #{i}:")
            print("-" * 40)
            for key, value in article.items():
                if key == "URL":
                    print(f"{key}: {value} (ссылка на статью)")
                else:
                    print(f"{key}: {value}")
        print("=" * 80)
    else:
        print(news_info)