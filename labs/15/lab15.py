from fastapi import FastAPI
import wikipedia as wik
from pydantic import BaseModel

app = FastAPI()

@app.get('/{summary}')
def wiki_summary(summary: str):
    '''Выводит суммарную информацию по введённому запросу'''
    return "Суммарная информация: " + wik.summary(summary)

@app.get('/search/')
def wiki_search(search: str, request: int=0):
    '''Находит и выводит определённое количество заданных(похожих) заголовков статей'''
    return f"Заголовки по запросу {search}: " + ', '.join(wik.search(search, request))

class Request(BaseModel):
    title: str
    img: int

@app.post('/')
def wiki_search_img(wiki_img: Request):
    '''Даёт нужное изображение из статьи'''
    return Request(title=wik.page(wiki_img.title).images[wiki_img.img-1], img=wiki_img.img)