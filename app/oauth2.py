import jwt
from jwt.exceptions import InvalidTokenError
from . import schemas
from fastapi import Depends,status, HTTPException
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# tokenUrl="login" does not automatically call or connect to your /login route — it is just a declaration used by the OpenAPI docs (Swagger at /docs) to know:
# "Hey, if someone wants a token, tell them to POST to /login."
# So this is only for documentation/UI purposes, not functional logic.

#Secret key
#algorithm
#expiration time for token

SECRET_KEY = "77t87gg87g8556c6dgus7g8yvo76fv56dfr545oju786fvyuinoiuhy67"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=[ALGORITHM])

    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokeData(id = id)
    except InvalidTokenError:
        raise credentials_exception

#what this going to do is, we can pass this as a dependency in any one of our path operations.
#it is going to take the token from the request automatically and extracts the id for us and going to verify the token is correct
# when this get_current_user runs in any path operation which we want to protect, then Depends(oauth2_scheme) runs
#  -->   It uses OAuth2PasswordBearer
#   -->  Looks in the Authorization header
#   -->  Extracts the Bearer token

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials"
                                          ,headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token,credentials_exception)
