import speech_recognition as sr 

class SpeechText:
    def __init__(self, mode):
        self.mode = mode

        if self.mode == 'api':
            self.recognizer = sr.Recognizer()

    def _api_recognition(self,audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)

        return self.recognizer.recognize_google(audio)

    def _local_recognition(self,audio_file):
        return "Hello"

    def recognize(self,audio_file):
        if self.mode == 'api':
            return self._api_recognition(audio_file)
        if self.mode == 'local':
            return self._local_recognition(audio_file)