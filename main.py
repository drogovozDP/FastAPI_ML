from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle

app = FastAPI()
# обслуживание статических файлов
app.mount('/static', StaticFiles(directory='static'), name='static')
# обслуживание страницы через шаблонизаторы
templates = Jinja2Templates(directory='templates')

with open("lin_reg.pkl", 'rb') as file:
    lin_reg = pickle.load(file)

def model(x):
    query = [[x['day']] + [0 for i in range(24)]]
    query[0][x['hour'] + 1] = 1
    return round(lin_reg.predict(query)[0], 2)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/', response_class=HTMLResponse)
async def index(request: Request, date: str = Form(...), time: str = Form(...)):
    day = int(date[-2:])
    hour = int(time[0:2])
    message = model({'day': day, 'hour': hour})
    return templates.TemplateResponse('index.html', {'request': request, 'message': message})


# if __name__ == '__main__':
#     uvicorn.run('main:app')