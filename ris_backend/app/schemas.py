# This file is a serializer
from pydantic import BaseModel, Field, ValidationError, conint, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime, date
from uuid import UUID
from enum import Enum

# ------------------------ NEW


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    others = "others"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role_id: Optional[str] = None


class User(BaseModel):
    role_id: conint(ge=0)
    username: str
    full_name: str
    gender: GenderEnum
    dob: date
    created_at: datetime
    is_active: bool = True


class UserInDB(User):
    password: str


# ------------------------ OLD


class StaffRoleBase(BaseModel):
    role_name: str


class StaffRoleCreate(StaffRoleBase):
    pass


class AuthResponse(BaseModel):
    role_id: conint(ge=0)


class StaffRole(StaffRoleBase):
    role_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)


class StaffAccountBase(BaseModel):
    username: str
    full_name: str
    gender: GenderEnum
    dob: date
    created_at: datetime
    is_active: bool = True


class StaffAccountCreate(StaffAccountBase):
    password: str
    role_id: conint(ge=0)


class StaffAccount(StaffAccountBase):
    staff_id: UUID
    role_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)


class TableBase(BaseModel):
    capacity: conint(ge=2)
    is_available: bool = True


class TableCreate(TableBase):
    pass


class Table(TableBase):
    table_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    table_id: conint(ge=0)
    staff_id: UUID
    is_served: bool = False
    created_at: datetime

    # @field_validator('table_id')
    # def check_table_exists(cls, value):
    #     session: Session = SessionLocal()
    #     result = session.execute(
    #         text("SELECT * FROM tables WHERE table_id = :table_id"), {'table_id': value})
    #     table = result.mappings().first()
    #     session.close()
    #     if not table:
    #         raise ValueError('table_id must associate with an existing table')
    #     return value

    # @field_validator('staff_id')
    # def check_waiter_role(cls, value):
    #     session: Session = SessionLocal()
    #     result = session.execute(text(
    #         "SELECT * FROM staff_accounts WHERE staff_id = UNHEX(REPLACE(:staff_id, '-', ''))"), {'staff_id': str(value)})
    #     staff = result.mappings().first()
    #     session.close()
    #     if not staff or staff['role_id'] != 1:
    #         raise ValueError('staff_id must belong to a waiter (role_id == 1)')
    #     return value


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DishBase(BaseModel):
    order_id: UUID
    staff_id: UUID
    menu_item_id: UUID
    note: Optional[str] = None
    quantity: conint(gt=0)
    total: float
    is_ready: bool = False

    @field_validator('total')
    def total_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('total must be greater than 0')
        return value

    # @field_validator('order_id')
    # def check_order_exists(cls, value):
    #     session: Session = SessionLocal()
    #     result = session.execute(text(
    #         "SELECT * FROM orders WHERE order_id = UNHEX(REPLACE(:order_id, '-', ''))"), {'order_id': str(value)})
    #     order = result.mappings().first()
    #     session.close()
    #     if not order:
    #         raise ValueError('order_id must associate with an existing order')
    #     return value

    # @field_validator('staff_id')
    # def check_chef_role(cls, value):
    #     session: Session = SessionLocal()
    #     result = session.execute(text(
    #         "SELECT * FROM staff_accounts WHERE staff_id = UNHEX(REPLACE(:staff_id, '-', ''))"), {'staff_id': str(value)})
    #     staff = result.mappings().first()
    #     session.close()
    #     if not staff or staff['role_id'] != 2:
    #         raise ValueError('staff_id must belong to a chef (role_id == 2)')
    #     return value

    # @field_validator('menu_item_id')
    # def check_menu_item_exists(cls, value):
    #     session: Session = SessionLocal()
    #     result = session.execute(text(
    #         "SELECT * FROM menu_items WHERE menu_item_id = UNHEX(REPLACE(:menu_item_id, '-', ''))"), {'menu_item_id': str(value)})
    #     menu_item = result.mappings().first()
    #     session.close()
    #     if not menu_item:
    #         raise ValueError(
    #             'menu_item_id must associate with an existing menu item')
    #     return value


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    dish_id: UUID

    model_config = ConfigDict(from_attributes=True)


class MenuItemBase(BaseModel):
    item_name: str
    note: Optional[str] = None
    price: float
    menu_section_id: conint(ge=0)

    # @field_validator('menu_section_id')
    # def check_menu_section_exists(cls, value):
    #     session: Session = SessionLocal()
    #     result = session.execute(text(
    #         "SELECT * FROM menu_sections WHERE menu_section_id = :menu_section_id"), {'menu_section_id': value})
    #     menu_section = result.mappings().first()
    #     session.close()
    #     if not menu_section:
    #         raise ValueError(
    #             'menu_section_id must associate with an existing menu section')
    #     return value


class MenuItemCreate(MenuItemBase):
    pass


class MenuItem(MenuItemBase):
    menu_item_id: UUID

    model_config = ConfigDict(from_attributes=True)


class MenuSectionBase(BaseModel):
    section_name: str


class MenuSectionCreate(MenuSectionBase):
    pass


class MenuSection(MenuSectionBase):
    menu_section_id: conint(ge=0)

    model_config = ConfigDict(from_attributes=True)
