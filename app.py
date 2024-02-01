from fastapi import FastAPI, Form
import uvicorn

from chat import ChatBot

app = FastAPI()

@app.post('/')
def get_answer(question: str = Form(...)):
    #function call
    answer = chat.invoke(question)
    return answer

if __name__ == '__main__':
    chat = ChatBot("content.txt")
    uvicorn.run(app, host="0.0.0.0", port=8000)
