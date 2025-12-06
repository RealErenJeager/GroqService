from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

class ChatRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_groq(req: ChatRequest):
    try:
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are a tech expert. Answer only technology-related questions."},
                {"role": "user", "content": req.question}
            ],
            "temperature": 0.2
        }

        response = requests.post(URL, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
