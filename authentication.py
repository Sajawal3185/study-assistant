from passlib.hash import bcrypt 
from datetime import datetime, timezone, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def get_password_hash(password: str) -> str:
    hash = bcrypt.hash(password)
    return hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_verification = bcrypt.verify(plain_password,hashed_password)
    return password_verification

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    try:
     payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
     print("Your token is expired")
     return None
    except jwt.InvalidTokenError:
       print("Invalid token")
       return None
    else:
       return payload

token = create_access_token({"sub":"test@example.com"})
result = decode_access_token(token)
print(result)

result = decode_access_token("not.a.real.token")
