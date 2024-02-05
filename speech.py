import speech_recognition as sr 
import requests
import time
import pyttsx3

class SpeechQuery:

    def __init__(self,api_url, listening_callback = None, waiting_callback = None):
        self.api_url = api_url
        self.__listening_callback = listening_callback
        self.__waiting_callback = waiting_callback

        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()

        #TODO: Add recorder configuration
        # self.r.energy_threshold = None
        # self.r.pause_threshold = None

        #Voice Engine Configuration
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',voices[1].id)
    
    def set_voice(self, voice_index):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',voices[voice_index].id)

    def __send_request(self,text):
        if self.__waiting_callback: self.__waiting_callback()

        print("Sending Request...")
        t = time.time()
        response = requests.post(self.api_url, json = {'query': text})
        print(f"Took {time.time() - t} seconds.")
        print(response.text)
        return response.json().get('body').strip()
    
    def __get_audio(self):
        if self.__listening_callback: self.__listening_callback()
        with sr.Microphone() as src:
            print("Starting to listen...")
            audio = self.r.listen(src, phrase_time_limit = 10, timeout = 5)
            print("Completed Listening")
        
        return audio
    
    def __get_text(self,audio):
        print("Recogonizing Speech")
        question = self.r.recognize_google(audio)
        print(question)
        return question
    
    def __speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen_and_reply(self):
        audio = self.__get_audio()
        text = self.__get_text(audio)
        answer = self.__send_request(text)
        self.__speak(answer)
        return answer