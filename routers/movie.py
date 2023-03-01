# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# typing for special models
from typing import List

#local libraries management
## Token management
from utils.jwt_manager import create_token
from middlewares.jwt_bearer import JWTBearer
## Databse connection
from config.database import Session
## Models
from models.movie import Movie as MovieModel
#Services
from services.movie import MovieService
# Schemas / models
from schemas.movie import Movie


movie_router =  APIRouter()


@movie_router.get('/movies', 
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
    results = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(results), status_code=status.HTTP_200_OK)


@movie_router.get(path="/movies/{id}",
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
    movie = MovieService(db).get_movie_by_Id(id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return JSONResponse(content = jsonable_encoder(movie), status_code=status.HTTP_200_OK)


@movie_router.get('/movies/', 
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
    results  =  MovieService(db).get_movies_by_category(category)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
    return JSONResponse(content = jsonable_encoder(results), status_code=status.HTTP_200_OK)


@movie_router.post('/movies', 
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
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message":"Movie has been added succesfuly"}, status_code=status.HTTP_201_CREATED)


@movie_router.put('/movies/{id}', 
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
    result = MovieService(db).get_movie_by_Id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content = jsonable_encoder(movie), status_code=status.HTTP_200_OK)


@movie_router.delete('/movies/{id}', 
            tags=['movies'], 
            response_model=dict,
            status_code=status.HTTP_200_OK,
            summary="Delete a movie")
def delete_movie(id: int) -> dict:        
    db = Session()
    result = MovieService(db).get_movie_by_Id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message":"Movie deleted succesfuly"}, status_code=status.HTTP_200_OK)