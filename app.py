from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import uvicorn
import time,datetime
import csv
import os

from chat import ChatBot
from speech import SpeechText
from speak import TextSpeech

app = FastAPI()

@app.post('/feedback')
def save_feedback(audio_file: UploadFile = File(...), name: str = Form(...)):
    t = time.time()
    try:
        question = speech.recognize(audio_file.file)
        with open(log_file,'a') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.datetime.now(), name, question, "Feedback"])
    except:
        return 404
    return 200

@app.post('/')
def get_answer(audio_file: UploadFile = File(...), name: str = Form(...)):

    t = time.time()
    try:
        question = speech.recognize(audio_file.file)
    except:
        return 0
    
    print(f"Took {time.time() - t} seconds for speech recognition. {question}" )
    answer = chat.ask(question, name)
    answer = answer.replace("AWS","Ae W S")
    answer = answer.replace("AI","Ae I")
    print(f"Took {time.time() - t} seconds till generating output. {answer}")
    audio = speaker.render(answer)
    print(f"Took {time.time() - t} seconds in total.")
    with open(log_file,'a') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), name, question, answer])
    return FileResponse(audio)

if __name__ == '__main__':
    speech = SpeechText()
    speaker = TextSpeech()
    chat = ChatBot("context.txt")
    log_file = os.path.join('logs',f'log{time.time()}.csv')
    with open(log_file,'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Date Time", "Asker","Question", "Response"])
        
    uvicorn.run(app, host="0.0.0.0", port=8000)
