# This file is a data validator / serializer in Django
from pydantic import BaseModel, Field, ValidationError, conint, ConfigDict, field_validator
from typing import List, Optional, Dict
from datetime import datetime, date
from uuid import UUID
from enum import Enum

# ------------------------ ENUMS ------------------------


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    others = "others"


class TableStatusEnum(str, Enum):
    vacant = 'vacant'
    reserved = 'reserved'
    eating = 'eating'


class DishStatusEnum(str, Enum):
    received = 'received'
    prepared = 'prepared'
    ready = 'ready'

# ------------------------ AUTHENTICATION SCHEMAS ------------------------


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

# ------------------------ USER SCHEMAS ------------------------


class User(BaseModel):
    role_id: conint(ge=0)
    staff_id: UUID
    username: str
    full_name: str
    gender: GenderEnum
    dob: date
    created_at: datetime
    is_active: bool = True


class UserInDB(User):
    password: str

# ------------------------ TABLE SCHEMAS ------------------------


class TableStatusUpdate(BaseModel):
    table_id: int


class TableBase(BaseModel):
    capacity: conint(ge=2)
    table_status: TableStatusEnum


class Table(TableBase):
    table_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)

# ------------------------ ORDER SCHEMAS ------------------------


class OrderBase(BaseModel):
    table_id: conint(ge=0)
    staff_id: UUID
    is_served: bool = False
    created_at: datetime


class OrderCreate(BaseModel):
    table_id: int
    staff_id: UUID


class Order(OrderBase):
    order_id: UUID

    model_config = ConfigDict(from_attributes=True)


class OrderItemDetail(BaseModel):
    item_name: str
    quantity: int
    price: float


class OrderDetail(BaseModel):
    order_id: UUID
    items: List[OrderItemDetail]
    created_at: datetime
    is_served: bool


class OrderUpdate(BaseModel):
    order_id: UUID
    table_id: int
    is_served: bool

    model_config = ConfigDict(from_attributes=True)

# ------------------------ DISH SCHEMAS ------------------------


class DishBase(BaseModel):
    order_id: UUID
    staff_id: UUID
    menu_item_id: UUID
    note: Optional[str] = None
    quantity: conint(gt=0)
    total: float
    dish_status: DishStatusEnum

    @field_validator('total')
    def total_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('total must be greater than 0')
        return value


class DishCreate(BaseModel):
    menu_item_id: UUID
    quantity: conint(gt=0)


class OrderWithDishesCreate(BaseModel):
    table_id: conint(ge=0)
    dishes: List[DishCreate]


class Dish(DishBase):
    dish_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DishDisplay(BaseModel):
    dish_id: UUID
    order_id: UUID
    table_id: int
    item_name: str
    quantity: int
    dish_status: DishStatusEnum

    model_config = ConfigDict(from_attributes=True)


class DishStatusUpdate(BaseModel):
    dish_id: UUID

# ------------------------ MENU ITEM SCHEMAS ------------------------


class MenuItemBase(BaseModel):
    item_name: str
    note: Optional[str] = None
    price: float
    menu_section_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)


class MenuItemCreate(MenuItemBase):
    pass


class MenuItem(MenuItemBase):
    menu_item_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    menu_item_id: UUID
    item_name: str
    note: Optional[str] = None
    price: float
    model_config = ConfigDict(from_attributes=True)


# ------------------------ MENU SECTION SCHEMAS ------------------------


class MenuSectionBase(BaseModel):
    section_name: str
    model_config = ConfigDict(from_attributes=True)


class MenuSectionCreate(MenuSectionBase):
    pass


class MenuSection(MenuSectionBase):
    menu_section_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)


class MenuSectionWithItems(MenuSectionBase):
    menu_section_id: conint(ge=0)
    menu_items: List[ItemBase]

    model_config = ConfigDict(from_attributes=True)
