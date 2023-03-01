from jwt import encode, decode
from dotenv import load_dotenv
import os

load_dotenv()

secret_env_key = os.getenv('SECRET_KEY')

def create_token(data: dict) -> str:
    token: str = encode(payload=data,
                        key=secret_env_key,
                        algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=secret_env_key, algorithms=['HS256'])
    return data