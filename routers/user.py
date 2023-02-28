# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Pydantic for model handling
from pydantic import BaseModel

#local libraries management
## Token management
from jwt_manager import create_token


user_router =  APIRouter()


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

@user_router.post("/login",
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