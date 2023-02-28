# FastAPI
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

# Pydantic for model handling
from pydantic import BaseModel, Field

# typing for special models
from typing import Optional, List

#local libraries management
## Token management
from jwt_manager import create_token
from middlewares.jwt_bearer import JWTBearer
## Databse connection
from config.database import Session, engine, Base
## Models
from models.movie import Movie as MovieModel
## Erro handling
from middlewares.error_handler import ErrorHandler



app = FastAPI()
app.title =  "My FastAPI app"
app.version = "0.1.0"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)



class User(BaseModel):
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "123456"
            }
        }

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=50, min_length=5)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023, gt=1900)
    rating: float = Field(ge=1.0, le=10.0)
    category: str = Field(min_length=5, max_length=15)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My movie",
                "overview": "Movie's description ...",
                "year": 2023,
                "rating": 9.8,
                "category": "Acción"
            }
        }

movies = [
        {
            'id': 1,
            'title': 'Avatar',
            'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
            'year': 'status.HTTP_200_OK9',
            'rating': 7.8,
            'category': 'Acción'    
        },
        {
            'id': 2,
            'title': 'Interestalar',
            'overview': "Hanz zimmer",
            'year': '2010',
            'rating': 10.0,
            'category': 'espacial'    
        } 
    ]


@app.get('/',
         tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


@app.post("/login",
          tags=["auth"],
          summary="User login, get JWT")
def login(user: User):
    """User Login

    - Args:
        - user (User): Email and password correctly to obtain the token

    - Returns:
        - Token: str
    """
    if (user.email == "admin@gmail.com" and user.password == "123456"):
        print(user.dict())
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})


@app.get('/movies', 
         tags=["movies"], 
         response_model=List[Movie],
         status_code=status.HTTP_200_OK,
         dependencies=[Depends(JWTBearer())],
         summary="Shows all movies")
def get_movies() -> List[Movie]:
    """Get Movies

    - Returns:
        - List[Movie]: A list with all the movies
    """
    db = Session()
    results = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(results), status_code=status.HTTP_200_OK)


@app.get(path="/movies/{id}",
         tags=["movies"],
         summary="Show a movie in the app",
         response_model=Movie)
def get_movie(id: int = Path(ge=1, le=5000)):
    """Get a movie
    
    - Params:
        - id: int
        
    - Returns a json with de basic movie information
        - id: int
        - title: str
        - overview: str
        - year: int
        - rating: int
        - category: str
    """
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return JSONResponse(content = jsonable_encoder(movie), status_code=status.HTTP_200_OK)


@app.get('/movies/', 
         tags=['movies'],
         response_model=List[Movie],
         summary="Query by category") 
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    """Get movies by category

    - Args:
        - category (str, optional): Category you are looking for. Defaults to Query(min_length=5, max_length=15).

    - Raises:
        - HTTPException: 404 Not found. In case no movie is found with that category

    - Returns:
        - List[Movie]: All the movies with that category
    """
    db = Session()
    results  =  db.query(MovieModel).filter(MovieModel.category == category).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
    return JSONResponse(content = jsonable_encoder(results), status_code=status.HTTP_200_OK)


@app.post('/movies', 
          tags=['movies'], 
          response_model=dict,
          status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    """Create Movie

    -Args:
        - movie (Movie): Movie schema in json format

    - Returns:
        - dict: Message movie created or not
    """
    db = Session()
    newMovie = MovieModel(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={"message":"Movie has been added succesfuly"}, status_code=status.HTTP_201_CREATED)


@app.put('/movies/{id}', 
         tags=['movies'], 
         response_model=dict,
         status_code=status.HTTP_200_OK)
def update_movie(id: int, movie: Movie) -> dict:
    """Update Movie

    - Args:
        - id (int): id of the specific movie to update
        - movie (Movie): Movie model in json format with all data, including the one not be changed

    - Raises:
        - HTTPException: 404 NOT Found. No movie found with that id

    - Returns:
        - dict: movie information sent
    """
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    result.title = movie.title
    result.category = movie.category
    result.overview = movie.overview
    result.rating = movie.rating
    result.year = movie.year  
    db.commit()
    return JSONResponse(content = jsonable_encoder(movie), status_code=status.HTTP_200_OK)

@app.delete('/movies/{id}', 
            tags=['movies'], 
            response_model=dict,
            status_code=status.HTTP_200_OK,
            summary="Delete a movie")
def delete_movie(id: int) -> dict:        
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message":"Movie deleted succesfuly"}, status_code=status.HTTP_200_OK)