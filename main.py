# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

# Pydantic for model handling
from pydantic import BaseModel

#local libraries management
## Token management
from jwt_manager import create_token
## Databse connection
from config.database import Session, engine, Base
## Erro handling
from middlewares.error_handler import ErrorHandler

#Routers
from routers.movie import movie_router
from routers.user import user_router


app = FastAPI()
app.title =  "My FastAPI app"
app.version = "0.1.0"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get('/',
         tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


