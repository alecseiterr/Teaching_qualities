import pandas as pd
import matplotlib.pyplot as plt

def process_emotional_tone(data_path, new_data_path, file_path_to_save):
    data = pd.read_csv(data_path)

    llm_data = pd.read_csv(new_data_path)

    merged_data = data.merge(llm_data[['ID урока','Нецензурные_выражения', 'Технические_неполадки', 'Жалобы_на_качество', 
                                       'Критика_методов_преподавания', 'Предложения_по_улучшению', 
                                       'Проблемы_с_пониманием_материала', 'Технические_проблемы_LLM', 
                                       'Жалобы_на_качество_LLM', 'Критика_методов_преподавания_LLM', 
                                       'Предложения_по_улучшению_LLM', 'Проблемы_с_пониманием_материала_LLM', 
                                       'Эмоциональный_тон_LLM', 'Отзыв_LLM']], on='ID урока', how='left')


    merged_data.to_csv(file_path_to_save, index=False, encoding='utf-8-sig')

    unique_emotional_tones = merged_data['Эмоциональный_тон_LLM'].unique()

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