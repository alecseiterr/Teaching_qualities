```markdown
# Teaching_qualities

## Введение
Контролируем качество преподавания с использованием искусственного интеллекта.

## Установка

### Клонирование репозитория
```
git clone git@github.com:alecseiterr/Teaching_qualities.git
```

### Настройка виртуального окружения
Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/Scripts/activate  # Для Windows используйте venv\Scripts\activate
```

### Установка зависимостей
Установите необходимые зависимости из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Скачивание LLM модели
Скачайте модель LLM по ссылке и разместите в директории с файлом `main.py`:
[Скачать модель](https://huggingface.co/TheBloke/openchat-3.5-0106-GGUF/resolve/main/openchat-3.5-0106.Q8_0.gguf)

### Запуск приложения
```bash
python main.py
```
После запуска выберите файл для анализа и изучите графики и сформированные классы и характеристики лекциы.

## Дополнительная информация

### Системные требования
Программа проверена на операционной системе Windows 11. Для корректной работы рекомендуется установить пакеты Desktop development with C++ и Windows 11 SDK через Visual Studio Installer.

### Производительность
Обучение модели на полном датасете проходило на GPU Nvidia 4090 в течение 5 часов. Работа предикта с общим датасетом занимает около 6 минут на том же оборудовании.

## Команда проекта

- **Александр Чернышов** - [Telegram](https://t.me/Chernyshov_Aleksandr)
- **Алексей Терещенко** - [Telegram](https://t.me/AlecseiTer)
- **Дмитрий Шульцев** - [Telegram](https://t.me/VikingSPb78)
- **Светлана Лунева** - [Telegram](https://t.me/SvetlanaLuneva1)
- **Артем Резер** - [Telegram](https://t.me/artyom_rezer)

```
