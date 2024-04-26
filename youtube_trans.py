from pytube import YouTube
from pydub import AudioSegment
import logging
import speech_recognition as sr
import os
# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_audio(youtube_link, output_filename):
    try:
        yt = YouTube(youtube_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download(filename=output_filename)
            logging.info(f"Аудио успешно загружено: {output_filename}")
            return output_filename
        else:
            logging.error("Аудиопоток не найден")
            raise Exception("Аудиопоток не найден")
    except Exception as e:
        logging.error(f"Не удалось загрузить аудио: {e}")
        raise


def convert_to_wav(input_file, output_file):
    try:
        sound = AudioSegment.from_file(input_file)
        sound = sound.set_frame_rate(16000)
        sound.export(output_file, format="wav")
        logging.info(f"Файл конвертирован в WAV: {output_file}")
    except Exception as e:
        logging.error(f"Не удалось конвертировать файл в WAV: {e}")
        raise


def load_bad_words(filename):
    """Загрузка списка запрещённых слов из файла, где слова разделены запятыми."""
    with open(filename, 'r', encoding='utf-8') as file:
        # Считывание всего файла и разделение слов по запятым
        bad_words = file.read().strip().lower().split(',')
        # Удаление возможных пробелов вокруг слов
        bad_words = [word.strip() for word in bad_words]
    return set(bad_words)


def check_for_bad_words(text, bad_words):
    """Проверка текста на наличие запрещённых слов."""
    words = text.lower().split()
    found_bad_words = set(words) & bad_words
    if found_bad_words:
        logging.warning(f"Обнаружены запрещённые слова: {', '.join(found_bad_words)}")
        return True
    return False


def split_audio(file_path, duration=60000):
    """Разбивает аудио на сегменты заданной длительности."""
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i+duration] for i in range(0, len(audio), duration)]
    return chunks


def transcribe_audio(audio_chunk, language="ru-RU"):
    """Транскрибирует отдельный аудио-сегмент."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        logging.error("Google Speech Recognition не смогло распознать аудио")
    except sr.RequestError as e:
        logging.error(f"Не удалось получить результаты от сервиса Google Speech Recognition; {e}")
    return ""


def transcribe(file_path, language="ru-RU", output_file="transcription.txt", bad_words_file="bad_words.txt"):
    """Транскрибация всего файла с дозаписью в текстовый файл."""
    bad_words = load_bad_words(bad_words_file)
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i+60000] for i in range(0, len(audio), 60000)]

    for i, chunk in enumerate(chunks):
        chunk_file = f"temp_chunk{i}.wav"
        chunk.export(chunk_file, format="wav")
        text = transcribe_audio(chunk_file, language)
        os.remove(chunk_file)

        if text:
            if check_for_bad_words(text, bad_words):
                logging.warning("Обнаружены запрещённые слова в аудио сегменте.")
            # Дозапись текста в файл
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(text + " ")


# Пример использования
if __name__ == "__main__":
    try:
        youtube_link = "https://www.youtube.com/watch?v=gIlMnYA-YJA"
        output_filename = "downloaded_audio.mp4"
        wav_filename = "converted_audio.wav"

        output_text_file = "transcription.txt"

        # Загрузка и конвертация аудио
        downloaded_file = download_audio(youtube_link, output_filename)
        convert_to_wav(downloaded_file, wav_filename)
        transcribe(wav_filename)

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
