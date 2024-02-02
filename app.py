from fastapi import FastAPI, UploadFile, File
import uvicorn

from chat import ChatBot
from speech import SpeechText

app = FastAPI()

@app.post('/')
def get_answer(audio_file: UploadFile = File(...)):

    question = speech.recognize(audio_file.file)
    answer = chat.invoke(question)
    return answer

if __name__ == '__main__':
    chat = ChatBot("content.txt")
    speech = SpeechText()
    uvicorn.run(app, host="0.0.0.0", port=8000)
