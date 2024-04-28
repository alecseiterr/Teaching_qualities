import pandas as pd
import numpy as np

#Вернемся к исходному датафрейму
file_path = 'analis.csv'
data = pd.read_csv(file_path)

# Удаление строк, где 'ID урока' пропущен
data = data.dropna(subset=['ID урока'])

# Замена пустых строк на NaN
data['Дата старта урока'].replace('', np.nan, inplace=True)

# Попытка преобразовать столбец 'Дата старта урока' в datetime, обработка некорректных значений
data['Дата старта урока'] = pd.to_datetime(data['Дата старта урока'], errors='coerce')

# Проверка, сколько теперь значений NaN после очистки и преобразования
missing_after_conversion = data['Дата старта урока'].isnull().sum()

# Преобразование 'Дата сообщения' в datetime, обработка ошибок
data['Дата сообщения'] = pd.to_datetime(data['Дата сообщения'], errors='coerce')

# Замена пропущенных значений в 'Дата сообщения' значениями из 'Дата старта урока'
data['Дата сообщения'] = data['Дата сообщения'].fillna(data['Дата старта урока'])

# Группировка данных по 'ID урока' и нахождение максимальной 'Дата сообщения' для каждого урока
max_message_date = data.groupby('ID урока')['Дата сообщения'].max()

# Присоединение результата к основному DataFrame
# data = data.merge(max_message_date.rename('Максимальная дата сообщения'), on='ID урока')

# Вычисление длительности урока
data['Длительность урока'] = data['Максимальная дата сообщения'] - data['Дата старта урока']


# Группировка данных по 'ID урока' и подсчёт количества сообщений для каждого урока
message_count = data.groupby('ID урока')['Текст сообщения'].count()

# Присоединение количества сообщений к основному DataFrame
data = data.merge(message_count.rename('Количество сообщений'), on='ID урока')

# Преобразование длительности урока в минуты
data['Длительность урока в минутах'] = data['Длительность урока'].dt.total_seconds() / 60

# Расчет плотности сообщений в минуту
data['Плотность сообщений в минуту'] = data['Количество сообщений'] / data['Длительность урока в минутах']

# Замена бесконечных значений на NaN, если длительность урока равна 0
data['Плотность сообщений в минуту'].replace([float('inf'), -float('inf')], pd.NA, inplace=True)


import pandas as pd
import matplotlib.pyplot as plt

# Извлечение часа из 'Дата старта урока'
data['Час старта урока'] = data['Дата старта урока'].dt.hour

# Группировка данных по часу и расчет средней плотности сообщений
hourly_density = data.groupby('Час старта урока')['Плотность сообщений в минуту'].mean()

# Визуализация результатов
plt.figure(figsize=(10, 6))
hourly_density.plot(kind='bar')
plt.title('Средняя плотность сообщений по часам')
plt.xlabel('Час дня')
plt.ylabel('Средняя плотность сообщений в минуту')
plt.xticks(rotation=0)
plt.grid(True)
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
# Загрузка дополнительных метрик по урокам из файла
new_data_path = '/content/new_data.csv'
new_data = pd.read_csv(new_data_path)

merged_data = data.merge(llm_data[['ID урока','Нецензурные_выражения',	'Технические_неполадки',	'Жалобы_на_качество',	'Критика_методов_преподавания',	'Предложения_по_улучшению',	'Проблемы_с_пониманием_материала',	'Технические_проблемы_LLM',	'Жалобы_на_качество_LLM',	'Критика_методов_преподавания_LLM',	'Предложения_по_улучшению_LLM',	'Проблемы_с_пониманием_материала_LLM',	'Эмоциональный_тон_LLM',	'Отзыв_LLM']], on='ID урока', how='left')


# Сохранение датафрейма в CSV-файл
file_path_to_save = 'analis.csv'  # Укажи здесь путь и имя файла
merged_data.to_csv(file_path_to_save, index=False, encoding='utf-8-sig')


# Получение уникальных значений в столбце 'эмоциональный_тон'
unique_emotional_tones = merged_data['Эмоциональный_тон_LLM'].unique()


# Удаление всех строк, которые не являются числовыми значениями 1 или 0
clean_emotional_tone = merged_data['Эмоциональный_тон_LLM'].replace(to_replace=[None], value=np.nan)
clean_emotional_tone = pd.to_numeric(clean_emotional_tone, errors='coerce').dropna()

# Проверяем ещё раз уникальные значения после очистки
print("Уникальные значения после очистки:")
print(clean_emotional_tone.unique())

# Подсчёт частоты появления 1
if 1 in clean_emotional_tone.values:
    positive_tone_count = merged_data[merged_data['Эмоциональный_тон_LLM'].astype(str).str.contains('1')].groupby('Час старта урока').size()
    plt.figure(figsize=(12, 6))
    positive_tone_count.plot(kind='bar')
    plt.title('Частота положительного эмоционального тона (1) по часам суток')
    plt.xlabel('Час дня')
    plt.ylabel('Количество')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
else:
    print("Значения 1 в столбце 'эмоциональный_тон' не обнаружено после очистки.")