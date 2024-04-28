import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def process_emotional_tone(data_path, new_data_path, file_path_to_save):

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