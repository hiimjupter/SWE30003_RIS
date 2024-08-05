import pytest
from pydantic import ValidationError
from datetime import datetime, date
from uuid import uuid4, UUID
from app.schemas import User, DishDisplay, Dish, DishStatusUpdate, GenderEnum, DishStatusEnum

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
            role_id=-1,  # Invalid role_id
            staff_id=uuid4(),
            username="testuser",
            full_name="Test User",
            gender=GenderEnum.male,
            dob=date(1990, 1, 1),
            created_at=datetime.now(),
            is_active=True
        )


def test_dish_display_schema():
    dish_display = DishDisplay(
        dish_id=uuid4(),
        order_id=uuid4(),
        table_id=1,
        item_name="Pizza",
        quantity=2,
        dish_status=DishStatusEnum.prepared
    )
    assert dish_display.item_name == "Pizza"
    with pytest.raises(ValidationError):
        DishDisplay(
            dish_id=uuid4(),
            order_id=uuid4(),
            table_id=1,
            item_name="Pizza",
            quantity=-2,
            dish_status=DishStatusEnum.prepared
        )


def test_dish_schema():
    dish = Dish(
        dish_id=uuid4(),
        order_id=uuid4(),
        staff_id=uuid4(),
        menu_item_id=uuid4(),
        note="No onions",
        quantity=3,
        total=29.99,
        dish_status=DishStatusEnum.received
    )
    assert dish.total == 29.99
    with pytest.raises(ValidationError):
        Dish(
            dish_id=uuid4(),
            order_id=uuid4(),
            staff_id=uuid4(),
            menu_item_id=uuid4(),
            note="No onions",
            quantity=3,
            total=-29.99,  # Invalid total
            dish_status=DishStatusEnum.received
        )


def test_dish_status_update_schema():
    dish_status_update = DishStatusUpdate(
        dish_id=uuid4()
    )
    assert isinstance(dish_status_update.dish_id, UUID)
    with pytest.raises(ValidationError):
        DishStatusUpdate(
            dish_id="invalid-uuid"  # Invalid UUID
        )


if __name__ == "__main__":
    pytest.main()
