from jose import JWTError, jwt
from datetime import *


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    encoded_data =data.copy()

    expiry_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp": expiry_time})
    jwt_token= jwt.encode(encoded_data,SECRET_KEY,ALGORITHM)
    return jwt_token
