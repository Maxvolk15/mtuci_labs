from fastapi import FastAPI
import pyjokes
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def joke():
    return pyjokes.get_joke()

@app.get('/{friend}')
def friends_joke(friend: str):
    return friend + ' шутканул: ' + pyjokes.get_joke()

@app.get('/multi/{friend}')
def multi_friends_joke(friend: str, jokes_num: int):
    result=''
    for i in range(jokes_num):
        result += friend + f' шутканул свою {i+1} шутку: ' + pyjokes.get_joke() + ' '
    return result

class Joke(BaseModel):
    friend: str
    joke: str

class JokeInp(BaseModel):
    friend: str

@app.post('/')
def create_joke(joke_in: JokeInp):
    return Joke(friend=joke_in.friend, joke=pyjokes.get_joke())

@app.post('/', response_model=Joke)
def create_joke(joke_inp: JokeInp):
    '''Creating joke'''
    return Joke(friend=joke_inp.friend, joke=pyjokes.get_joke())