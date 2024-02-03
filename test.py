import speech_recognition as sr
import time
import requests
# obtain audio from the microphone
r = sr.Recognizer()
# r.energy_threshold = 900
# r.pause_threshold = 900
with sr.Microphone(device_index=0) as source:
    print(source.device_index)
    print("Say something!")
    audio = r.listen(source,phrase_time_limit=5,timeout=5)


url = 'https://a2cd-104-196-245-8.ngrok-free.app/ask'

headers = {
    'accept': 'application/json',
}

files = {
    'audio_file': ('audio.wav',audio.get_wav_data() , 'audio/wav'),
}

t = time.time()
response = requests.post(url, headers=headers, files=files)
print(time.time() - t)
print(response.text)