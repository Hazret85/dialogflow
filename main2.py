import os
import speech_recognition as sr
from gtts import gTTS
import playsound
import google.cloud.dialogflow_v2 as dialogflow


# Укажи путь к JSON ключу для API Dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "famous-team-405108-9801d86a6ee1.json"


def speak(text):
    tts = gTTS(text=text, lang='ru')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажи что-нибудь...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            print("Не понял, повторите...")
            return ""
        except sr.RequestError:
            print("Ошибка соединения")
            return ""


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input
    )

    return response.query_result.fulfillment_text


def handle_command(command):
    # Используем Dialogflow для обработки команд
    project_id = "__nothing__"  # Замените на ваш project ID в Dialogflow
    session_id = "123456"  # Можно использовать случайный ID для каждой сессии

    response = detect_intent_texts(project_id, session_id, command, 'ru')

    if response:
        print(f"Ответ Dialogflow: {response}")
        speak(response)
    else:
        print("Dialogflow не распознал запрос")
        speak("Извините, я не понимаю эту команду.")


if __name__ == "__main__":
    command = listen()
    if command:
        handle_command(command)
