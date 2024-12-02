import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Параметры нормального распределения
mean = 0 # Среднее значение
std_dev = 1 # Стандартное отклонение
num_samples = 1000 # Количество образцов

# Генерация случайных чисел, распределенных по нормальному распределению
data = np.random.normal(mean, std_dev, num_samples)

# Построение гистограммы
plt.figure(figsize=(8, 6))
plt.hist(data, bins=30, edgecolor='black')
plt.title('Гистограмма случайных данных, распределенных по нормальному распределению')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.savefig('normal_distribution_histogram.png')
plt.show()

# Генерация двух наборов случайных данных
random_array1 = np.random.rand(100)
random_array2 = np.random.rand(100)

# Построение диаграммы рассеяния
plt.figure(figsize=(8, 6))
plt.scatter(random_array1, random_array2)
plt.title('Диаграмма рассеяния случайных данных')
plt.xlabel('Данные 1')
plt.ylabel('Данные 2')
plt.savefig('scatter_plot_random_data.png')
plt.show()

# URL категории диванов
base_url = 'https://www.divan.ru/category/divany-i-kresla'

# Отправка GET-запроса
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Поиск элементов с диванами
divans = soup.find_all(['div', 'article'], class_=re.compile('product|item|card'))

# Список для хранения данных
data = []

for divan in divans:
    try:
        # Поиск названия и цены
        name_elem = divan.find('h3') or divan.find('div', class_=re.compile('name|title')) or divan.find('a', class_=re.compile('name|title'))
        name = name_elem.get_text(strip=True) if name_elem else 'Без названия'

        price_elem = divan.find('span', class_=re.compile('price|стоимость|cost')) or divan.find('div', class_=re.compile('price|стоимость|cost'))
        price = int(re.sub(r'[^\d]', '', price_elem.get_text(strip=True))) if price_elem else 0

        if price > 0:
            data.append({
                'Название': name,
                'Цена': price
            })
    except Exception as e:
        print(f"Ошибка при обработке элемента: {e}")

# Создание DataFrame
df = pd.DataFrame(data)

# Сохранение в CSV
df.to_csv('divany_prices.csv', index=False, encoding='utf-8')

# Вычисление средней цены
mean_price = df['Цена'].mean()
print(f"Средняя цена на диваны: {mean_price:.2f} руб.")

# Построение гистограммы
plt.figure(figsize=(8, 6))
plt.hist(df['Цена'], bins=30, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (руб.)')
plt.ylabel('Количество')
plt.savefig('divany_price_histogram.png')
plt.show()