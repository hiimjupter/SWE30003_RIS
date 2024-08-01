import pytest
from pydantic import ValidationError
from uuid import UUID
from datetime import datetime, date
from app.schemas import (
    GenderEnum,
    StaffRole,
    StaffRoleCreate,
    StaffAccount,
    StaffAccountCreate,
    Table,
    TableCreate,
    Order,
    OrderCreate,
    Dish,
    DishCreate,
    MenuItem,
    MenuItemCreate,
    MenuSection,
    MenuSectionCreate,
)

# Test cases


def test_staff_role_schema():
    for role in roles_data:
        role_model = StaffRole(**role)
        assert isinstance(role_model, StaffRole)
        assert role_model.role_id == role["role_id"]
        assert role_model.role_name == role["role_name"]


def test_staff_account_schema():
    for account in staff_accounts_data:
        account["staff_id"] = UUID(account["staff_id"])
        account_model = StaffAccount(**account)
        assert isinstance(account_model, StaffAccount)
        assert account_model.username == account["username"]
        assert account_model.gender == GenderEnum(account["gender"])
        assert isinstance(account_model.gender, GenderEnum)


def test_table_schema():
    for table in tables_data:
        table_model = Table(**table)
        assert isinstance(table_model, Table)
        assert table_model.table_id == table["table_id"]
        assert table_model.capacity == table["capacity"]


def test_order_schema():
    for order in orders_data:
        order["order_id"] = UUID(order["order_id"])
        order["staff_id"] = UUID(order["staff_id"])
        order_model = Order(**order)
        assert isinstance(order_model, Order)
        assert order_model.table_id == order["table_id"]
        assert not order_model.is_served


def test_dish_schema():
    for dish in dishes_data:
        dish["dish_id"] = UUID(dish["dish_id"])
        dish["order_id"] = UUID(dish["order_id"])
        dish["staff_id"] = UUID(dish["staff_id"])
        dish["menu_item_id"] = UUID(dish["menu_item_id"])
        dish_model = Dish(**dish)
        assert isinstance(dish_model, Dish)
        assert dish_model.quantity == dish["quantity"]
        assert dish_model.total == dish["total"]


def test_menu_item_schema():
    for item in menu_items_data:
        item["menu_item_id"] = UUID(item["menu_item_id"])
        item_model = MenuItem(**item)
        assert isinstance(item_model, MenuItem)
        assert item_model.item_name == item["item_name"]
        assert item_model.price == item["price"]


def test_menu_section_schema():
    for section in menu_sections_data:
        section_model = MenuSection(**section)
        assert isinstance(section_model, MenuSection)
        assert section_model.section_name == section["section_name"]

# Test invalid cases


def test_invalid_role_id():
    with pytest.raises(ValidationError):
        StaffAccountCreate(
            username="test_user",
            full_name="Test User",
            gender="male",
            dob=date(2000, 1, 1),
            created_at=datetime.now(),
            is_active=True,
            password="test_password",
            role_id=-1,
        )


def test_invalid_gender():
    with pytest.raises(ValidationError):
        StaffAccountCreate(
            username="test_user",
            full_name="Test User",
            gender="Male",
            dob=date(2000, 1, 1),
            created_at=datetime.now(),
            is_active=True,
            password="test_password",
            role_id=-1,
        )


def test_invalid_capacity():
    with pytest.raises(ValidationError):
        TableCreate(capacity=1, is_available=True)


def test_invalid_quantity():
    with pytest.raises(ValidationError):
        DishCreate(
            order_id=UUID("550e8400-e29b-41d4-a716-446655440002"),
            staff_id=UUID("550e8400-e29b-41d4-a716-446655440001"),
            menu_item_id=UUID("550e8400-e29b-41d4-a716-446655440006"),
            note="Test",
            quantity=0,
            total=10.0,
            is_ready=False,
        )


def test_invalid_total():
    with pytest.raises(ValidationError):
        DishCreate(
            order_id=UUID("550e8400-e29b-41d4-a716-446655440002"),
            staff_id=UUID("550e8400-e29b-41d4-a716-446655440001"),
            menu_item_id=UUID("550e8400-e29b-41d4-a716-446655440006"),
            note="Test",
            quantity=1,
            total=-10.0,
            is_ready=False,
        )
