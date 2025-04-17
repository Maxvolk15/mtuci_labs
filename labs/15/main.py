from fastapi import FastAPI
import pyjokes

app = FastAPI()

@app.get('/')
def joke():
    return pyjokes.get_joke()