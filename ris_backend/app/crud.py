import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from uuid import UUID

from . import models, schemas
from app.database import SessionLocal

# Load variables from constants
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# Load password context & authentication scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Role-based Access Control Functions


def verify_password(plain_password, hashed_password):
    # Compare client's password and password in database
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    # Hash given password with bcrypt algorithm
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    # Get user matching with given username
    return db.query(models.StaffAccount).filter(models.StaffAccount.username == username).first()


def authenticate_user(db: Session, username: str, password: str):

    # Get user with given username
    user = get_user(db, username)
    # No user exists with username
    if not user:
        return None
    # User's password (database) is not matching with client's password
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Get data to encode
    to_encode = data.copy()
    # Provide checking on session duration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Encode the data and session duration
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Table-related functions


def get_tables(db: Session):
    return db.query(models.Table).all()


def get_table(db: Session, table_id: int):
    # Get table matching with given table_id
    return db.query(models.Table).filter(models.Table.table_id == table_id).first()


def get_menu_items(db: Session):
    return db.query(models.MenuItem).all()


def get_menu_item(db: Session, menu_item_id: UUID):
    return db.query(models.MenuItem).filter(
        models.MenuItem.menu_item_id == menu_item_id).first()


def get_dish(db: Session, dish_id: UUID):
    return db.query(models.Dish).filter(models.Dish.dish_id == dish_id).first()


def get_dish_by_order(db: Session, order_id: UUID):
    return db.query(models.Dish).filter(
        models.Dish.order_id == order_id
    ).all()


def get_exist_unserved_orders(db: Session, table_id: int, is_served: bool):
    return db.query(models.Order).filter(
        models.Order.table_id == table_id,
        models.Order.is_served == is_served
    ).all()


def get_sorted_order_by_table(db: Session, table_id: int):
    return db.query(models.Order).filter(
        models.Order.table_id == table_id
    ).order_by(models.Order.created_at.desc()).first()


def get_menu_sections(db: Session):
    return db.query(models.MenuSection).all()


def get_menu_items_by_sections(db: Session, menu_section_id: int):
    return db.query(models.MenuItem).filter(
        models.MenuItem.menu_section_id == menu_section_id).all()


def get_section_name(db: Session, section_name: str):
    return db.query(models.MenuSection).filter(
        models.MenuSection.section_name == section_name).first()