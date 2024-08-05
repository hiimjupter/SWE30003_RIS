import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime, date
from app.schemas import (
    User, UserInDB, Token, TokenData,
    Table, TableStatusUpdate,
    Order, OrderCreate, OrderItemDetail, OrderDetail, OrderUpdate,
    Dish, DishCreate, OrderWithDishesCreate, DishDisplay, DishStatusUpdate,
    MenuItem, MenuItemCreate, MenuSection, MenuSectionCreate, MenuSectionWithItems,
    GenderEnum, TableStatusEnum, DishStatusEnum
)


def test_user_schema():
    user_data = {
        "role_id": 1,
        "staff_id": uuid4(),
        "username": "john_doe",
        "full_name": "John Doe",
        "gender": "male",
        "dob": date(1990, 1, 1),
        "created_at": datetime.now(),
        "is_active": True
    }
    user = User(**user_data)
    assert user.username == "john_doe"

    with pytest.raises(ValidationError):
        user_data_invalid = user_data.copy()
        user_data_invalid["role_id"] = -1
        User(**user_data_invalid)


def test_user_in_db_schema():
    user_data = {
        "role_id": 1,
        "staff_id": uuid4(),
        "username": "john_doe",
        "full_name": "John Doe",
        "gender": "male",
        "dob": date(1990, 1, 1),
        "created_at": datetime.now(),
        "is_active": True,
        "password": "securepassword"
    }
    user_in_db = UserInDB(**user_data)
    assert user_in_db.password == "securepassword"


def test_token_schema():
    token_data = {
        "access_token": "someaccesstoken",
        "token_type": "bearer"
    }
    token = Token(**token_data)
    assert token.token_type == "bearer"
