import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def process_emotional_tone(data_path):

    clean_emotional_tone = pd.read_csv(data_path)
    clean_emotional_tone = merged_data['Эмоциональный_тон_LLM'].replace(to_replace=[None], value=np.nan)
    clean_emotional_tone = pd.to_numeric(clean_emotional_tone, errors='coerce').dropna()

    print("Уникальные значения после очистки:")
    print(clean_emotional_tone.unique())

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