import pandas as pd
import os
from langchain_community.llms import LlamaCpp


def process_with_llm(file_path):
    # Загрузка модели LLM
    model_path = 'openchat-3.5-0106.Q8_0.gguf'
    if os.path.exists(model_path):
        model = LlamaCpp(model_path=model_path,
                         n_gpu_layers=50,
                         n_batch=512,
                         n_ctx=8192,
                         temperature=0.1)
        print("Model loaded successfully.")
    else:
        print(f"Model path does not exist: {model_path}")
        return None

    # Загрузка данных из файла
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        print(data.head())  # Выведем первые несколько строк для проверки
    else:
        print(f"Data file does not exist: {file_path}")
        return None

    # Добавление новых столбцов к датафрейму
    new_columns = {
        'Технические_проблемы_LLM': [''] * len(data),
        'Жалобы_на_качество_LLM': [''] * len(data),
        'Критика_методов_преподавания_LLM': [''] * len(data),
        'Предложения_по_улучшению_LLM': [''] * len(data),
        'Проблемы_с_пониманием_материала_LLM': [''] * len(data),
        'Эмоциональный_тон_LLM': [''] * len(data),
        'Отзыв_LLM': [''] * len(data),
    }

    # Добавление новых столбцов к датафрейму
    data = data.assign(**new_columns)

    def generate_response(text):
        answer = model(f'GPT4 Correct User: {text}GPT4 Correct Assistant:')
        return str(answer)

    # Анализ каждой строки датафрейма с помощью LLM
    for index, row in data.iterrows():
        try:
            text = row['Текст_сообщения']
            if len(text) < 3000:
                data.at[index, 'Технические_проблемы_LLM'] = generate_response(
                    f'Lesson messages text: {text}\n\nDoes the feedback mention contains any technical issue? If yes write 1, if no write 0')
                data.at[index, 'Жалобы_на_качество_LLM'] = generate_response(
                    f'Lesson messages text: {text}\n\nDoes the feedback mention any quality complaints? If yes write 1, if no write 0')
                data.at[index, 'Критика_методов_преподавания_LLM'] = generate_response(
                    f'Lesson messages text: {text}\n\nDoes the feedback contain criticism of teaching methods? If yes write 1, if no write 0')
                data.at[index, 'Предложения_по_улучшению_LLM'] = generate_response(
                    f'Lesson messages text: {text}\n\nDoes the feedback contain suggestions for improvement? If yes write 1, if no write 0')
                data.at[index, 'Проблемы_с_пониманием_материала_LLM'] = generate_response(
                    f'Lesson messages text: {text}\n\nDoes the feedback mention problems with understanding the material? If yes write 1, if no write 0')
                data.at[index, 'Эмоциональный_тон_LLM'] = generate_response(
                    f'Lesson messages text: {text}\n\nIs the overall emotional tone of the feedback negative(0) or positive(1)? If negative write 0, if positive write 1. Dont write anything else.')
                data.at[index, 'Отзыв_LLM'] = generate_response(
                    f'Текст сообщений урока: {text}\n\nОставь краткий отзыв об уроке судя по сообщенияем учеников.')

            data.to_csv('new_data.csv', index=False)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Открываем обновленный датафрейм после анализа с помощью LLM
    file_path = 'new_data.csv'
    llm_data = pd.read_csv(file_path)

    llm_data = llm_data.dropna(subset=['ID урока'])
    print(llm_data.info())

    return llm_data


def data_new(file_path):
    file_path = 'analis.csv'
    llm_data = pd.read_csv(file_path)

    llm_data = llm_data.dropna(subset=['ID урока'])
    print(llm_data.info())

    return llm_data


# Пример использования функции
# llm_data = process_with_llm('mergedataframe.csv')
