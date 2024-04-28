import pandas as pd
import re
import os


def process_feedback_table(file_path):
    try:
        data = pd.read_excel(file_path, engine='openpyxl')
        # Если загрузка прошла успешно и не возникло ошибок, выведем сообщение об успешной загрузке
        print("Файл успешно загружен!")
    except ValueError as e:
        # Если возникла ошибка ValueError, это означает проблемы при загрузке файла
        print("Ошибка загрузки файла:", e)
        # Попытаемся загрузить файл без заголовков, если предыдущий метод не сработал
        data = pd.read_excel(file_path, header=None)

    # Удаление точки с запятой из всех строк столбца 'Текст сообщения'
    data['Текст сообщения'] = data['Текст сообщения'].str.replace(';', '')

    # Посмотреть первые несколько строк датафрейма
    print(data.head())

    # Создадим функции для проверки каждого из критериев
    def contains_profanity(text):
        # Замени на реальные нецензурные слова
        profanity_list = ['badword1', 'badword2']
        return any(profanity in text.lower() for profanity in profanity_list)

    def contains_tech_issues(text):
        tech_keywords = ['не работает', 'ошибка', 'глюк']
        return any(keyword in text.lower() for keyword in tech_keywords)

    def contains_quality_complaint(text):
        quality_keywords = ['плохое качество', 'не могу понять', 'скучно']
        return any(keyword in text.lower() for keyword in quality_keywords)

    def contains_teaching_critique(text):
        teaching_keywords = ['метод', 'подход', 'неэффективно']
        return any(keyword in text.lower() for keyword in teaching_keywords)

    def contains_improvement_suggestion(text):
        improvement_keywords = ['предлагаю', 'лучше бы', 'было бы хорошо']
        return any(keyword in text.lower() for keyword in improvement_keywords)

    def contains_understanding_issue(text):
        understanding_keywords = ['не понимаю', 'сложно', 'можно повторить']
        return any(keyword in text.lower() for keyword in understanding_keywords)


    # Переименование столбца для удобства обращения к нему
    data.rename(columns={'Текст сообщения': 'Текст_сообщения'}, inplace=True)

    # Преобразование всех значений столбца в строки
    data['Текст_сообщения'] = data['Текст_сообщения'].astype(str)

    # После переименования и преобразования столбца применяем функции
    data['Нецензурные_выражения'] = data['Текст_сообщения'].apply(contains_profanity)
    data['Технические_неполадки'] = data['Текст_сообщения'].apply(contains_tech_issues)
    data['Жалобы_на_качество'] = data['Текст_сообщения'].apply(contains_quality_complaint)
    data['Критика_методов_преподавания'] = data['Текст_сообщения'].apply(contains_teaching_critique)
    data['Предложения_по_улучшению'] = data['Текст_сообщения'].apply(contains_improvement_suggestion)
    data['Проблемы_с_пониманием_материала'] = data['Текст_сообщения'].apply(contains_understanding_issue)

    # Удаление столбца 'Unnamed: 5'
    # data.drop(columns=['Unnamed: 6'], inplace=True)

    # Удаление столбца 'Размктка'
    data.drop(columns=['Разметка'], inplace=True)

    # Подсчет количества сообщений для каждого 'ID урока'
    messages_per_lesson = data['ID урока'].value_counts().to_dict()

    # Создание столбца 'плотность_откликов' с использованием подсчитанного количества сообщений
    data['плотность_откликов'] = data['ID урока'].apply(lambda x: messages_per_lesson.get(x, 0))

    # Среднее количество откликов на урок
    average_responses_per_lesson = data['плотность_откликов'].mean()

    # Максимальное количество откликов на урок
    max_responses_per_lesson = data['плотность_откликов'].max()

    # Минимальное количество откликов на урок
    min_responses_per_lesson = data['плотность_откликов'].min()

    # Вывод результатов
    print(f"Среднее количество откликов на урок: {average_responses_per_lesson}")
    print(f"Максимальное количество откликов на урок: {max_responses_per_lesson}")
    print(f"Минимальное количество откликов на урок: {min_responses_per_lesson}")

    # Сохранение датафрейма в CSV-файл
    file_path_to_save = 'my_dataframe.csv'  # Укажи здесь путь и имя файла
    data.to_csv(file_path_to_save, index=False, encoding='utf-8-sig')

    print(f"Данные сохранены в файл: {file_path_to_save}")

    # Сначала создаем агрегированный датафрейм для текста сообщений
    grouped_data = data.groupby('ID урока')['Текст_сообщения'].apply(' '.join).reset_index()

    # Добавляем плотность откликов из исходного датафрейма
    grouped_data = grouped_data.merge(data[['ID урока', 'плотность_откликов']].drop_duplicates(), on='ID урока', how='left')

    # Преобразовываем объединенные тексты сообщений в строки
    grouped_data['Текст_сообщения'] = grouped_data['Текст_сообщения'].astype(str)

    # Применяем функции к объединенным текстам сообщений
    grouped_data['Нецензурные_выражения'] = grouped_data['Текст_сообщения'].apply(contains_profanity)
    grouped_data['Технические_неполадки'] = grouped_data['Текст_сообщения'].apply(contains_tech_issues)
    grouped_data['Жалобы_на_качество'] = grouped_data['Текст_сообщения'].apply(contains_quality_complaint)
    grouped_data['Критика_методов_преподавания'] = grouped_data['Текст_сообщения'].apply(contains_teaching_critique)
    grouped_data['Предложения_по_улучшению'] = grouped_data['Текст_сообщения'].apply(contains_improvement_suggestion)
    grouped_data['Проблемы_с_пониманием_материала'] = grouped_data['Текст_сообщения'].apply(contains_understanding_issue)

    # Выводим результат
    print(grouped_data.head())
    # Сохранение датафрейма в CSV-файл
    file_path_to_save = 'mergedataframe.csv'  # Укажи здесь путь и имя файла
    grouped_data.to_csv(file_path_to_save, index=False, encoding='utf-8')

    print(f"Данные сохранены в файл: {file_path_to_save}")
    return grouped_data

# processed_data = process_feedback_table('train_GB_KachestvoPrepodovaniya1.xlsx')