from fastapi import FastAPI, UploadFile, File
import uvicorn
import time

from chat import ChatBot
from speech import SpeechText

app = FastAPI()

@app.post('/')
def get_answer(audio_file: UploadFile = File(...)):
    t = time.time()
    question = speech.recognize(audio_file.file)
    print(f"Took {time.time() - t} seconds for speech recognition.")
    answer = chat.invoke(question)
    print(f"Took {time.time() - t} seconds on total.")
    return answer

if __name__ == '__main__':
    chat = ChatBot("context.txt")
    speech = SpeechText()
    uvicorn.run(app, host="0.0.0.0", port=8000)
