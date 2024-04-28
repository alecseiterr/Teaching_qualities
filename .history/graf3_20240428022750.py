import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def process_emotional_tone(data_path):
    merged_data = pd.read_csv(data_path)
    merged_data['Дата старта урока'] = pd.to_datetime(merged_data['Дата старта урока'])

    merged_data['День'] = merged_data['Дата старта урока'].dt.day
    merged_data['Месяц'] = merged_data['Дата старта урока'].dt.month

    cols_to_sum = ['Технические_проблемы_LLM', 'Критика_методов_преподавания_LLM',
                'Жалобы_на_качество_LLM', 'Проблемы_с_пониманием_материала_LLM']

    for col in cols_to_sum:
        merged_data[col] = pd.to_numeric(merged_data[col], errors='coerce').fillna(0)

    grouped_data = merged_data.groupby(['Месяц', 'День'])[cols_to_sum].sum()

    march_data = grouped_data.loc[3]

    march_data.reset_index(inplace=True)

    lessons_per_day_march = merged_data[merged_data['Месяц'] == 3].groupby('День')['ID урока'].nunique()

    lessons_per_day_march_df = lessons_per_day_march.reset_index(name='Количество уроков')

    final_data = march_data.merge(lessons_per_day_march_df, on='День', how='left')

    ax = final_data.plot(x='День', y=['Технические_проблемы_LLM', 'Критика_методов_преподавания_LLM', 'Жалобы_на_качество_LLM', 'Проблемы_с_пониманием_материала_LLM'], kind='bar', stacked=True, figsize=(14, 7))
    final_data.plot(x='День', y='Количество уроков', secondary_y=True, ax=ax, color='green', marker='o')

    plt.title('Ежедневное количество проблем и уроков за март')
    plt.xlabel('День')
    plt.ylabel('Количество')
    plt.legend(title='Категория')
    plt.savefig('problem_plot.png', bbox_inches='tight')
    plt.show()


data_path = 'analis.csv'
process_emotional_tone(data_path)