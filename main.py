from fastapi import Body, FastAPI, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title =  "My FastAPI app"
app.version = "0.1.0"

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

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
            'year': '2009',
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

@app.get('/movies', tags=["movies"])
def get_movies():
    return movies

@app.get(path="/movies/{id}",
         tags=["movies"],
         summary="Show a movie in the app")
def get_movie(id: int = Path(ge=1, le=2000)):
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
    return movie


@app.get('/movies/', tags=['movies']) 
def get_movies_by_category(category: str, year: int = None):
    return [item for item in movies if item['category'] == category]

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
        
    return HTTPException(status_code=404, detail="Movie not found")

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
        
    return HTTPException(status_code=404, detail="Movie not found")