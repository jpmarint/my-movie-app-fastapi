from fastapi import Body, FastAPI, HTTPException, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title =  "My FastAPI app"
app.version = "0.1.0"


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


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', 
         tags=["movies"], 
         response_model=List[Movie],
         status_code=status.HTTP_200_OK)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=status.HTTP_200_OK)

@app.get(path="/movies/{id}",
         tags=["movies"],
         summary="Show a movie in the app",
         response_model=Movie)
def get_movie(id: int = Path(ge=1, le=status.HTTP_200_OK)):
    """Get a movie
    
    - Params:
        id: int
        
    - Returns a json with de basic movie information
        id: int
        title: str
        overview: str
        year: int
        rating: int
        category: str
    """
    movie = [movie for movie in movies if movie['id'] == id]
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(content= movie)


@app.get('/movies/', 
         tags=['movies'],
         response_model=List[Movie]) 
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(content = data)


@app.post('/movies', 
          tags=['movies'], 
          response_model=dict,
          status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message":"Movie has been added succesfuly"}, status_code=status.HTTP_201_CREATED)


@app.put('/movies/{id}', 
         tags=['movies'], 
         response_model=dict,
         status_code=status.HTTP_200_OK)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={"message":"Movie has been updated succesfuly"}, status_code=status.HTTP_200_OK)
        
    return JSONResponse(content={"message":"Movie not found"}, status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/movies/{id}', 
            tags=['movies'], 
            response_model=dict,
            status_code=status.HTTP_200_OK)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Movie deleted succesfuly"}, status_code=status.HTTP_200_OK)
        
    return JSONResponse(content={"message":"Movie not found"}, status_code=status.HTTP_404_NOT_FOUND)