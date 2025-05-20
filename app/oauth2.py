from fastapi.security import OAuth2
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# name of the login endpoint has to be passed in...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # payload
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        id = str(id)

        if id is None:
            raise credentials_exception   
        token_data = id # schemas.TokenData(id=id) <- temporarily replaced his code with just -> id - getting Internal Server Error?

    except JWTError:
        raise credentials_exception
    
    return token_data

# to be passed as a dependency into any one of our path operations - to take the token from the request automatically,
# vefify the token is still valid by calling the function above, extract the id - and automatically fetch user data from the db if we wish
# this data can then be used as an argument / parameter to be passed into the path operation function etc.
# when the credentials run / if there is an issue with the JWT token we raise an exception...
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception) 

    user = db.query(models.User).filter(models.User.id == token).first() # <- getting an error from token.id in video? changed to token!

    return user # verify_access_token(token, credentials_exception)
    