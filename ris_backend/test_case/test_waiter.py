import pytest
from pydantic import ValidationError
from datetime import datetime, date
from uuid import uuid4
from app.schemas import User, Table, TableStatusUpdate, MenuItem, Order, OrderWithDishesCreate, OrderDetail, OrderUpdate, GenderEnum, TableStatusEnum, DishStatusEnum, DishCreate, OrderItemDetail

# ------------------------ TEST CASES ------------------------


def test_user_schema():
    user = User(
        role_id=1,
        staff_id=uuid4(),
        username="testuser",
        full_name="Test User",
        gender=GenderEnum.male,
        dob=date(1990, 1, 1),
        created_at=datetime.now(),
        is_active=True
    )
    assert user.username == "testuser"
    with pytest.raises(ValidationError):
        User(
            role_id=-1,
            staff_id=uuid4(),
            username="testuser",
            full_name="Test User",
            gender=GenderEnum.male,
            dob=date(1990, 1, 1),
            created_at=datetime.now(),
            is_active=True
        )


def test_table_schema():
    table = Table(
        table_id=1,
        capacity=4,
        table_status=TableStatusEnum.vacant
    )
    assert table.capacity == 4
    with pytest.raises(ValidationError):
        Table(
            table_id=1,
            capacity=1,
            table_status=TableStatusEnum.vacant
        )


def test_table_status_update_schema():
    table_status_update = TableStatusUpdate(
        table_id=1
    )
    assert table_status_update.table_id == 1
    with pytest.raises(ValidationError):
        TableStatusUpdate(
            table_id=-1
        )


def test_menu_item_schema():
    menu_item = MenuItem(
        menu_item_id=uuid4(),
        item_name="Pizza",
        price=12.99,
        menu_section_id=1
    )
    assert menu_item.item_name == "Pizza"
    with pytest.raises(ValidationError):
        MenuItem(
            menu_item_id=uuid4(),
            item_name="Pizza",
            price=-12.99,
            menu_section_id=-1
        )


def test_order_schema():
    order = Order(
        order_id=uuid4(),
        table_id=1,
        staff_id=uuid4(),
        is_served=False,
        created_at=datetime.now()
    )
    assert order.table_id == 1
    with pytest.raises(ValidationError):
        Order(
            order_id=uuid4(),
            table_id=-1,
            staff_id=uuid4(),
            is_served=False,
            created_at=datetime.now()
        )


def test_order_with_dishes_create_schema():
    order_with_dishes = OrderWithDishesCreate(
        table_id=1,
        dishes=[DishCreate(menu_item_id=uuid4(), quantity=2)]
    )
    assert order_with_dishes.table_id == 1
    assert len(order_with_dishes.dishes) == 1
    with pytest.raises(ValidationError):
        OrderWithDishesCreate(
            table_id=-1,
            dishes=[DishCreate(menu_item_id=uuid4(), quantity=2)]
        )


def test_order_detail_schema():
    order_detail = OrderDetail(
        order_id=uuid4(),
        items=[OrderItemDetail(item_name="Pizza", quantity=2, price=12.99)],
        created_at=datetime.now(),
        is_served=False
    )
    assert len(order_detail.items) == 1
    with pytest.raises(ValidationError):
        OrderDetail(
            order_id=uuid4(),
            items=[OrderItemDetail(
                item_name="Pizza", quantity=-2, price=12.99)],
            created_at=datetime.now(),
            is_served=False
        )


def test_order_update_schema():
    order_update = OrderUpdate(
        order_id=uuid4(),
        table_id=1,
        is_served=True
    )
    assert order_update.is_served == True
    with pytest.raises(ValidationError):
        OrderUpdate(
            order_id=uuid4(),
            table_id=-1,
            is_served=True
        )


if __name__ == "__main__":
    pytest.main()
