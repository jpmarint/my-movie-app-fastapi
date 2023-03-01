from pydantic import BaseModel, Field
from typing import Optional, List


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