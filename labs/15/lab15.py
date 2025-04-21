from fastapi import FastAPI
import wikipedia as wik
from pydantic import BaseModel

app = FastAPI()

@app.get('/{summary}')
def wik_summary(summary: str):
    '''Выводит суммарную информацию по введённому запросу'''
    return "Суммарная информация: " + wik.summary(summary)

@app.get('/wiki/{search}')
def wik_search(request: str):
    '''Выводит URL-адрес страницы с нужным запросом'''
    return "URL-страница: " + wik.page(request).url

class Request(BaseModel):
    img: str

@app.post('/')
def wiki_search_img(wiki_img: Request):
    '''Даёт первое изображение из статьи'''
    return "Ссылка на изображение: " + wik.page(wiki_img.img).images[0]