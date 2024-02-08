from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import uvicorn
import time

from chat import ChatBot
from speech import SpeechText
from speak import TextSpeech

app = FastAPI()

@app.post('/')
def get_answer(audio_file: UploadFile = File(...), name: str = Form(...)):

    t = time.time()
    try:
        question = speech.recognize(audio_file.file)
    except:
        return 0
    
    print(f"Took {time.time() - t} seconds for speech recognition. {question}" )
    answer = chat.ask(question, name)
    answer = answer.replace("AWS","A. W S")
    answer = answer.replace("AI","A. I")
    print(f"Took {time.time() - t} seconds till generating output. {answer}")
    audio = speaker.render(answer)
    print(f"Took {time.time() - t} seconds till pesurathu")

    return FileResponse(audio)

if __name__ == '__main__':
    speech = SpeechText()
    speaker = TextSpeech()
    chat = ChatBot("context.txt")
    uvicorn.run(app, host="0.0.0.0", port=8000)
