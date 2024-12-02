import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import time
import re
import random

def clean_price(price_text):
    """Очистка текста цены от лишних символов"""
    if not price_text:
        return 0
    price = re.sub(r'[^\d]', '', price_text)
    return int(price) if price else 0

def parse_divany():
    base_url = 'https://www.divan.ru/category/divany-i-kresla'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        divans = soup.find_all(['div', 'article'], class_=re.compile('product|item|card'))
        data = []

        for divan in divans:
            try:
                name_elem = (divan.find('h3') or
                             divan.find('div', class_=re.compile('name|title')) or
                             divan.find('a', class_=re.compile('name|title')))
                name = name_elem.get_text(strip=True) if name_elem else 'Без названия'

                price_elem = (divan.find('span', class_=re.compile('price|стоимость|cost')) or
                              divan.find('div', class_=re.compile('price|стоимость|cost')))
                price = clean_price(price_elem.get_text(strip=True) if price_elem else '0')

                if price > 0:
                    data.append({
                        'Название': name,
                        'Цена': price
                    })

            except Exception as item_error:
                print(f"Ошибка при обработке элемента: {item_error}")
            time.sleep(random.uniform(0.5, 2))  # Добавляем случайную задержку

        if not data:
            print("Не удалось найти данные. Возможно, страница изменилась.")
            return None

        df = pd.DataFrame(data)
        return df

    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

def analyze_data(df):
    if df is not None and not df.empty:
        df['Ценовая категория'] = pd.cut(df['Цена'],
                                         bins=[0, 50000, 100000, 200000, float('inf')],
                                         labels=['Эконом', 'Средний', 'Премиум', 'Люкс'])
        category_counts = df['Ценовая категория'].value_counts()
        print("\nРаспределение по ценовым категориям:")
        print(category_counts)

        plt.figure(figsize=(10, 6))
        category_counts.plot(kind='bar')
        plt.title('Распределение диванов по ценовым категориям')
        plt.xlabel('Ценовая категория')
        plt.ylabel('Количество')
        plt.tight_layout()
        plt.savefig('divany_price_categories.png')
        plt.close()

def main():
    print("Начало парсинга...")
    start_time = time.time()

    df = parse_divany()

    if df is not None:
        analyze_data(df)

    end_time = time.time()
    print(f"\nПарсинг завершен за {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    main()