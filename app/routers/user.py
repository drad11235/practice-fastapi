from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# email address and password values are accessed via the JSON-formatted-text / data transferred from the client to the server 
# as an (http verb) post request via the url/users - i.e. clicking on the ENDPOINT hyperlink of our API documentation -> 
# once accessed -> the values are stored in an object called user <- a Pydantic object since it is validated against the Pydantic model 
# UserCreate in schemas etc.

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # update the relevant attribute / change the state of the pydantic 'user' model i.e. user.password i.e. hash it...
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # n.b. **post.dict() unpacks the dictionary in this way etc -> email=user.email, password=user.password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):   
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")

    return user