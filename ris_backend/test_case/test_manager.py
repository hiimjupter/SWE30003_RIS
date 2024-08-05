import pytest
from uuid import uuid4
from datetime import datetime, date
from pydantic import ValidationError
from app.schemas import (User, MenuSectionWithItems, MenuSection,
                         MenuSectionCreate, MenuItem, MenuItemCreate,
                         GenderEnum)

# ------------------------ USER SCHEMA TESTS ------------------------


def test_user_schema_valid():
    user = User(
        role_id=1,
        staff_id=uuid4(),
        username="john_doe",
        full_name="John Doe",
        gender=GenderEnum.male,
        dob=date(1990, 1, 1),
        created_at=datetime.now(),
        is_active=True
    )
    assert user.username == "john_doe"
    assert user.gender == GenderEnum.male


def test_user_schema_invalid_role_id():
    with pytest.raises(ValidationError):
        User(
            role_id=-1,  # Invalid role_id
            staff_id=uuid4(),
            username="john_doe",
            full_name="John Doe",
            gender=GenderEnum.male,
            dob=date(1990, 1, 1),
            created_at=datetime.now(),
            is_active=True
        )

# ------------------------ MENU ITEM SCHEMA TESTS ------------------------


def test_menu_item_create_schema_valid():
    item = MenuItemCreate(
        item_name="Pizza",
        note="Extra cheese",
        price=9.99,
        menu_section_id=1
    )
    assert item.item_name == "Pizza"
    assert item.price == 9.99


def test_menu_item_create_schema_invalid_price():
    with pytest.raises(ValidationError):
        MenuItemCreate(
            item_name="Pizza",
            note="Extra cheese",
            price=-12.5,
            menu_section_id=1
        )

# ------------------------ MENU SECTION SCHEMA TESTS ------------------------


def test_menu_section_create_schema_valid():
    section = MenuSectionCreate(
        section_name="Main Course"
    )
    assert section.section_name == "Main Course"


def test_menu_section_schema_valid():
    section = MenuSection(
        menu_section_id=1,
        section_name="Desserts"
    )
    assert section.menu_section_id == 1
    assert section.section_name == "Desserts"


def test_menu_section_with_items_schema_valid():
    section_with_items = MenuSectionWithItems(
        menu_section_id=1,
        section_name="Appetizers",
        menu_items=[
            {"menu_item_id": uuid4(), "item_name": "Spring Rolls",
             "note": "Vegetarian", "price": 5.99},
            {"menu_item_id": uuid4(), "item_name": "Chicken Wings",
             "note": None, "price": 7.99},
        ]
    )
    assert section_with_items.section_name == "Appetizers"
    assert len(section_with_items.menu_items) == 2
    assert section_with_items.menu_items[0].item_name == "Spring Rolls"


def test_menu_section_with_items_schema_invalid_item_price():
    with pytest.raises(ValidationError):
        MenuSectionWithItems(
            menu_section_id=1,
            section_name="Appetizers",
            menu_items=[
                {"menu_item_id": uuid4(), "item_name": "Spring Rolls",
                 "note": "Vegetarian", "price": -5.99},  # Invalid price
            ]
        )
