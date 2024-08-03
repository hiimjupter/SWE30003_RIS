# This file handles all API endpoints
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import TypeDecorator, BINARY
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Annotated
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


def get_db():
    # Database dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- AUTHENTICATION & AUTHORIZATION UTILS ---------------------


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


# ------------------------ CUSTOM UUID ------------------------


class UUID(TypeDecorator):
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            # If the value is already a UUID, return its binary representation
            return value.bytes
        if isinstance(value, bytes):
            # If the value is already bytes, return it directly
            return value
        return uuid.UUID(value).bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(bytes=value)

# ------------------------ AUTHENTICATION ENDPOINT ------------------------


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

# ------------------------ WAITER ENDPOINTS ------------------------


@ app.get("/users/waiter", response_model=schemas.User)
# Get current waiter details
def get_data(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    return current_user


@app.get("/users/waiter/tables", response_model=List[schemas.Table])
# Get all tables
def get_tables(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    tables = crud.get_tables(db)
    return tables


@app.put("/users/waiter/tables/reserve", response_model=schemas.Table)
# Update table status to reserved
def update_table_status(update: schemas.TableStatusUpdate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    table = crud.get_table(db, update.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    if table.table_status == "vacant":
        table.table_status = "reserved"
    else:
        raise HTTPException(
            status_code=400, detail="Only vacant table can be reserved")

    db.commit()
    db.refresh(table)
    return table


@app.get("/users/waiter/tables/menu-items", response_model=List[schemas.MenuItem])
# Get menu items for a specific table
def get_menu_items(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    menu_items = crud.get_menu_items(db)
    return menu_items


@app.post("/users/waiter/create-order", response_model=schemas.Order)
# Create an order with dishes
def create_order_with_dishes(order_data: schemas.OrderWithDishesCreate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    # Check if there are any existing orders for the same table that have not been served
    existing_orders = crud.get_exist_unserved_orders(
        db, order_data.table_id, False)

    if existing_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create new order, please finish the previous order on the same table"
        )
    # Create the order
    new_order = models.Order(
        table_id=order_data.table_id,
        staff_id=current_user.staff_id,
        created_at=datetime.utcnow()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Create the dishes
    for dish_data in order_data.dishes:
        menu_item = crud.get_menu_item(db, dish_data.menu_item_id)
        if not menu_item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        total_price = menu_item.price * dish_data.quantity
        new_dish = models.Dish(
            order_id=new_order.order_id,
            staff_id=current_user.staff_id,
            menu_item_id=dish_data.menu_item_id,
            quantity=dish_data.quantity,
            total=total_price,
            dish_status='received'
        )
        db.add(new_dish)

    # Update the table status
    table = crud.get_table(db, order_data.table_id)
    if table:
        table.table_status = 'eating'
        db.add(table)
    else:
        raise HTTPException(status_code=404, detail="Table not found")

    db.commit()

    return new_order


@app.get("/users/waiter/tables/{table_id}/order", response_model=schemas.OrderDetail)
# Get order details for a specific table
def get_order_details(table_id: int, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    # Get the latest order for the table
    order = crud.get_sorted_order_by_table(db, table_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.is_served == True:
        raise HTTPException(status_code=400, detail="No order available")

    # Get the order items
    dishes = crud.get_dish_by_order(db, order.order_id)
    # Prepare the response
    order_items = [
        schemas.OrderItemDetail(
            item_name=dish.menu_item.item_name,
            quantity=dish.quantity,
            price=dish.menu_item.price
        ) for dish in dishes
    ]

    return schemas.OrderDetail(
        order_id=order.order_id,
        items=order_items,
        created_at=order.created_at,
        is_served=order.is_served
    )


@app.put("/users/waiter/orders/{table_id}/serve", response_model=List[schemas.OrderUpdate])
# Update order status to served
def update_order_status(
        table_id: int,
        current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])),
        db: Session = Depends(get_db)):
    # Fetch orders for the given table_id that are not yet served
    orders = crud.get_exist_unserved_orders(db, table_id, False)

    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No unserved orders found for table_id {table_id}"
        )

    # Update is_served status to True for each order and change dishes' status to 'ready'
    updated_orders = []
    for order in orders:
        order.is_served = True
        db.add(order)

        # Fetch and update dishes for the order
        dishes = db.query(models.Dish).filter(
            models.Dish.order_id == order.order_id
        ).all()

        for dish in dishes:
            dish.dish_status = "ready"
            db.add(dish)

        updated_orders.append(order)

    table = crud.get_table(db, table_id)
    table.table_status = "vacant"

    db.commit()

    return updated_orders

# ------------------------ CHEF ENDPOINTS ------------------------


@app.get("/users/chef", response_model=schemas.User)
# Get current chef details
def get_data(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[2])), db: Session = Depends(get_db)):
    return current_user


@app.get("/users/chef/dishes", response_model=List[schemas.DishDisplay])
# Get all dishes for the chef
def get_dishes(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[2])), db: Session = Depends(get_db)):
    dishes = db.query(
        models.Dish.dish_id,
        models.Dish.order_id,
        models.Order.table_id,
        models.MenuItem.item_name,
        models.Dish.quantity,
        models.Dish.dish_status
    ).join(models.Order, models.Order.order_id == models.Dish.order_id)\
     .join(models.Table, models.Table.table_id == models.Order.table_id)\
     .join(models.MenuItem, models.MenuItem.menu_item_id == models.Dish.menu_item_id).all()

    if not dishes:
        raise HTTPException(status_code=404, detail="No dishes found")

    return [schemas.DishDisplay(
        dish_id=dish.dish_id,
        order_id=dish.order_id,
        table_id=dish.table_id,
        item_name=dish.item_name,
        quantity=dish.quantity,
        dish_status=dish.dish_status
    ) for dish in dishes]


@app.put("/users/chef/dishes/status-update", response_model=schemas.Dish)
# Update dish status
def update_dish_status(update: schemas.DishStatusUpdate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[2])), db: Session = Depends(get_db)):
    dish = crud.get_dish(db, update.dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    if dish.dish_status == "received":
        dish.dish_status = "prepared"
    elif dish.dish_status == "prepared":
        dish.dish_status = "ready"
    else:
        raise HTTPException(
            status_code=400, detail="ready dishes cannot be changed!")

    db.commit()
    db.refresh(dish)
    return dish

# ------------------------ MANAGER ENDPOINTS ------------------------


@app.get("/users/manager/menu-sections", response_model=List[schemas.MenuSectionWithItems])
# Get menu sections with their items
def get_menu_sections(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[3])), db: Session = Depends(get_db)):
    menu_sections = crud.get_menu_sections(db)
    if not menu_sections:
        raise HTTPException(status_code=404, detail="No menu sections found")

    result = []
    for section in menu_sections:
        items = crud.get_menu_items_by_section(db, section.menu_section_id)
        # Convert SQLAlchemy models to Pydantic models
        pydantic_items = [schemas.MenuItem(
            **item.__dict__) for item in items]
        result.append(schemas.MenuSectionWithItems(
            menu_section_id=section.menu_section_id,
            section_name=section.section_name,
            menu_items=pydantic_items
        ))

    return result


@app.post("/users/manager/menu-sections", response_model=schemas.MenuSection)
# Create a new menu section
def create_menu_section(section_data: schemas.MenuSectionCreate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[3])), db: Session = Depends(get_db)):
    # Check if section name already exists
    existing_section = crud.get_section_name(db, section_data.section_name)
    if existing_section:
        raise HTTPException(
            status_code=400, detail="Section name must be unique")

    # Create new section
    new_section = models.MenuSection(section_name=section_data.section_name)
    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section


@app.post("/users/manager/menu-items", response_model=schemas.MenuItem)
# Create a new menu item
def create_menu_item(item_data: schemas.MenuItemCreate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[3])), db: Session = Depends(get_db)):
    # Check if the section exists
    section = db.query(models.MenuSection).filter(
        models.MenuSection.menu_section_id == item_data.menu_section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Menu section not found")

    new_item = models.MenuItem(
        menu_section_id=item_data.menu_section_id,
        item_name=item_data.item_name,
        note=item_data.note,
        price=item_data.price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@app.delete("/users/manager/menu-sections/{menu_section_id}/delete", status_code=204)
# Delete a menu section and all associated items
def delete_menu_section(menu_section_id: int, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[3])), db: Session = Depends(get_db)):
    section = db.query(models.MenuSection).filter(
        models.MenuSection.menu_section_id == menu_section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Menu section not found")
    # Delete all associated menu items
    db.query(models.MenuItem).filter(
        models.MenuItem.menu_section_id == menu_section_id).delete()
    # Delete the section
    db.delete(section)
    db.commit()
    return {"detail": "Menu section and associated items deleted"}


@app.delete("/users/manager/menu-items/{menu_item_id}/delete", status_code=204)
# Delete a menu item
def delete_menu_item(menu_item_id: str, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[3])), db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(
        models.MenuItem.menu_item_id == menu_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Menu item deleted"}


@app.put("/users/manager/menu-items/{menu_item_id}", response_model=schemas.MenuItem)
# Update a menu item
def update_menu_item(menu_item_id: str, item_data: schemas.MenuItemCreate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[3])), db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(
        models.MenuItem.menu_item_id == menu_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item.item_name = item_data.item_name
    item.note = item_data.note
    item.price = item_data.price
    db.commit()
    db.refresh(item)
    return item
