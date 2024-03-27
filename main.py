import json
import logging
import os
import random
import sys
import tempfile
import threading

import cv2
import requests
import simpleaudio
import speech_recognition
from openai import OpenAI

VOICE_VOX_HOST = "127.0.0.1"
VOICE_VOX_PORT = 50021
AVATAR_INFO = [
    {
        "video": "./Nene.mp4",
        "name": "ねね",
        "speaker": 60,
    },
    {
        "video": "./Rin.mp4",
        "name": "りん",
        "speaker": 10,
    },
]
AVATAR = AVATAR_INFO[random.randint(0, 1)]

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def speak(text, speaker=AVATAR["speaker"]):
    logging.info("processing voice vox...")
    params = (("text", text), ("speaker", speaker))
    logging.info("getting audio_query...")
    audio_query = requests.post(
        f"http://{VOICE_VOX_HOST}:{VOICE_VOX_PORT}/audio_query", params=params
    )

    logging.info("generating synthesis...")
    synthesis = requests.post(
        f"http://{VOICE_VOX_HOST}:{VOICE_VOX_PORT}/synthesis",
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(audio_query.json()),
    )

    logging.info("generating audio...")
    with tempfile.TemporaryDirectory() as tmp:
        with open(f"{tmp}/audio.wav", "wb") as f:
            f.write(synthesis.content)
            wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/audio.wav")
            play_obj = wav_obj.play()
            play_obj.wait_done()


def chat_with_chatgpt(prompt, chars=50):
    logging.info("asking chatGPT...")
    content = f"{chars}文字程度で教えてもらいたいです。" + prompt
    logging.info(content)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model="gpt-3.5-turbo",
    )
    content = chat_completion.choices[0].message.content
    speak(content)


def recognize_voice():
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    with microphone as source:
        logging.info("recognizing voice...")
        # recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
    try:
        logging.info("recognizing by google...")
        result = recognizer.recognize_google(audio, language="ja-JP")
        if not result:
            speak("何かおっしゃってください。")
        logger.info(result)
        chat_with_chatgpt(result)
    except speech_recognition.UnknownValueError as e:
        logger.error(e)
        speak("すいません。質問の意味が分かりませんでした。")
    except speech_recognition.RequestError as e:
        logger.error(e)
        speak("すいません。質問の意味が分かりませんでした。")


def run_ai():
    speak(f"こんにちは。{AVATAR['name']}です。何かご用ですか？")
    while True:
        recognize_voice()
        speak("ほかにご用はございますか？")


def display_video():
    cap = cv2.VideoCapture(AVATAR["video"])
    if not cap.isOpened():
        logger.error("cannot open")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    thread = threading.Thread(target=run_ai)
    thread.start()
    display_video()
