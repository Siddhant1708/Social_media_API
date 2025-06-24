import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta

#Secret key
#algorithm
#expiration time for token

SECRET_KEY = "77t87gg87g8556c6dgus7g8yvo76fv56dfr545oju786fvyuinoiuhy67"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt