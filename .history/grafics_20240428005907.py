import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_hourly_density(data):
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

def plot_positive_tone_count(data):
    # Получение уникальных значений в столбце 'эмоциональный_тон'
    unique_emotional_tones = data['Эмоциональный_тон_LLM'].unique()

    # Удаление всех строк, которые не являются числовыми значениями 1 или 0
    clean_emotional_tone = data['Эмоциональный_тон_LLM'].replace(to_replace=[None], value=np.nan)
    clean_emotional_tone = pd.to_numeric(clean_emotional_tone, errors='coerce').dropna()

    # Подсчёт частоты появления 1
    if 1 in clean_emotional_tone.values:
        positive_tone_count = data[data['Эмоциональный_тон_LLM'].astype(str).str.contains('1')].groupby(
            'Час старта урока').size()
        plt.figure(figsize=(12, 6))
        positive_tone_count.plot(kind='bar')
        plt.title('Частота положительного эмоционального тона (1) по часам суток')
        plt.xlabel('Час дня')
        plt.ylabel('Количество')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()

def analyze_and_save_plots(data_path, new_data_path, file_path_to_save):
    # Загрузка данных
    data = pd.read_csv(data_path)
    new_data = pd.read_csv(new_data_path)

    # Анализ и построение графика плотности сообщений по часам
    plot_hourly_density(data)
    plt.savefig(file_path_to_save.replace('.csv', '_hourly_density.png'))  # Сохранение графика
    plt.close()

    # Анализ и построение графика частоты положительного эмоционального тона
    plot_positive_tone_count(data)
    plt.savefig(file_path_to_save.replace('.csv', '_positive_tone_count.png'))  # Сохранение графика
    plt.close()

    # Объединение данных
    merged_data = data.merge(new_data[['ID урока', 'Нецензурные_выражения', 'Технические_неполадки', 'Жалобы_на_качество',
                                       'Критика_методов_преподавания', 'Предложения_по_улучшению',
                                       'Проблемы_с_пониманием_материала', 'Технические_проблемы_LLM',
                                       'Жалобы_на_качество_LLM', 'Критика_методов_преподавания_LLM',
                                       'Предложения_по_улучшению_LLM', 'Проблемы_с_пониманием_материала_LLM',
                                       'Эмоциональный_тон_LLM', 'Отзыв_LLM']], on='ID урока', how='left')

    # Сохранение датафрейма в CSV-файл
    merged_data.to_csv(file_path_to_save, index=False, encoding='utf-8-sig')

# Путь к данным и файлам
data_path = '/content/data.csv'
new_data_path = '/content/new_data.csv'
file_path_to_save = '/content/analis.csv'

# Запуск анализа и сохранение результатов
analyze_and_save_plots(data_path, new_data_path, file_path_to_save)