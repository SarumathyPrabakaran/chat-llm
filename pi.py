# import speech_recognition as sr
# import time
# import requests
import pyttsx3


# r = sr.Recognizer()
engine = pyttsx3.init()

# with sr.Microphone(device_index=0) as source:
#     print(source.device_index)
#     print("Say something!")
#     audio = r.listen(source,phrase_time_limit=5,timeout=5,)


# url = 'https://20cf-34-16-150-248.ngrok-free.app/ask'

# headers = {
#     'accept': 'application/json',
# }

# files = {
#     'audio_file': ('audio.wav',audio.get_wav_data() , 'audio/wav'),
# }

# print("Sending request")
# t = time.time()
# response = requests.post(url, headers=headers, files=files)
# print(time.time() - t)
# print(response.text)

# engine.say(response.json().get('answer'))
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.say("hello")
engine.runAndWait()