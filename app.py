from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import uvicorn
import time

from chat import ChatBot
from speech import SpeechText
from speak import Pesuda

app = FastAPI()

@app.post('/')
def get_answer(audio_file: UploadFile = File(...), name: str = Form(...)):

    t = time.time()
    try:
        question = speech.recognize(audio_file.file)
    except:
        return 0
    
    print(f"Took {time.time() - t} seconds for speech recognition.")
    answer = chat.ask(question, name)
    print(f"Took {time.time() - t} seconds till generating output.")
    audio = pesurathu.pesu(answer)
    print(f"Took {time.time() - t} seconds till pesurathu")

    return FileResponse(audio)

if __name__ == '__main__':
    chat = ChatBot("context.txt")
    speech = SpeechText()
    pesurathu = Pesuda()
    uvicorn.run(app, host="0.0.0.0", port=8000)
