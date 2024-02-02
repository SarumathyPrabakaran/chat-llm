import speech_recognition as sr

class SpeechText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def recognize(self,audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
        return self.recognizer.recognize_google(audio)
