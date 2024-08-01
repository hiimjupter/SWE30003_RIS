import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from . import crud, models, schemas
from .database import SessionLocal, engine

# Load variables from constants
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRED_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES"))
# Initialize models
models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Apply FastAPI framework
app = FastAPI()
# Allow CORS for all domains for demonstration purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[schemas.User, Depends(get_current_active_user)]):
        if user.role_id in self.allowed_roles:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission!"
        )


@app.post("/login", status_code=200, response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found", headers={
                            "WWW-Authenticate": "Bearer"})
    if user is False:
        raise HTTPException(status_code=400, detail="Incorrect password", headers={
                            "WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=15)
    access_token = crud.create_access_token(
        data={"username": user.username, "role_id": user.role_id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@ app.get("/users/me", response_model=schemas.User)
def get_data(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    return current_user
