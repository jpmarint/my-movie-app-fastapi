from fastapi import HTTPException, status

from models.movie import Movie as MovieModel
from schemas.movie import Movie


class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie_by_Id(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        newMovie = MovieModel(**movie.dict())
        self.db.add(newMovie)
        self.db.commit()
        return
    
    def update_movie(self, id: int, data: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        
        movie.title = data.title
        movie.category = data.category
        movie.overview = data.overview
        movie.rating = data.rating
        movie.year = data.year  
        
        self.db.commit()
        return
    
    def delete_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(movie)
        self.db.commit()
        return