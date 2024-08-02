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


class UUID(TypeDecorator):
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            # If the value is already a UUID, return its binary representation
            return value.bytes
        return uuid.UUID(value).bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(bytes=value)


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

# API Endpoints for Waiter


@ app.get("/users/waiter", response_model=schemas.User)
def get_data(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    return current_user


@app.get("/users/waiter/tables", response_model=List[schemas.Table])
def get_tables(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    return tables


@app.put("/users/waiter/tables/reserve", response_model=schemas.Table)
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


@app.get("/users/waiter/tables/{table_id}/menu-items", response_model=List[schemas.MenuItem])
def get_menu_items(table_id: int, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    elif table.table_status != "reserved":
        raise HTTPException(
            status_code=400, detail="Only reserved table can make order")
    else:
        menu_items = db.query(models.MenuItem).all()
    return menu_items


@app.post("/users/waiter/create-order", response_model=schemas.Order)
def create_order_with_dishes(order_data: schemas.OrderWithDishesCreate, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    # Check if there are any existing orders for the same table that have not been served
    existing_orders = db.query(models.Order).filter(
        models.Order.table_id == order_data.table_id,
        models.Order.is_served == False
    ).all()

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
        menu_item = db.query(models.MenuItem).filter(
            models.MenuItem.menu_item_id == dish_data.menu_item_id).first()
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
    table = db.query(models.Table).filter(
        models.Table.table_id == order_data.table_id).first()
    if table:
        table.table_status = 'eating'
        db.add(table)
    else:
        raise HTTPException(status_code=404, detail="Table not found")

    db.commit()

    return new_order


@app.get("/users/waiter/tables/{table_id}/order", response_model=schemas.OrderDetail)
def get_order_details(table_id: int, current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])), db: Session = Depends(get_db)):
    # Get the latest order for the table
    order = db.query(models.Order).filter(
        models.Order.table_id == table_id
    ).order_by(models.Order.created_at.desc()).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.is_served == True:
        raise HTTPException(status_code=400, detail="No order available")

    # Get the order items
    dishes = db.query(models.Dish).filter(
        models.Dish.order_id == order.order_id
    ).all()

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
def update_order_status(
    table_id: int,
    current_user: schemas.User = Depends(RoleChecker(allowed_roles=[1])),
    db: Session = Depends(get_db)
):
    # Fetch orders for the given table_id that are not yet served
    orders = db.query(models.Order).filter(
        models.Order.table_id == table_id,
        models.Order.is_served == False
    ).all()

    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No unserved orders found for table_id {table_id}"
        )

    # Update is_served status to True for each order
    updated_orders = []
    for order in orders:
        order.is_served = True
        order.updated_at = datetime.utcnow()
        db.add(order)
        updated_orders.append(order)

    db.commit()

    return updated_orders

# API Endpoints for Chef


@ app.get("/users/chef", response_model=schemas.User)
def get_data(current_user: schemas.User = Depends(RoleChecker(allowed_roles=[2])), db: Session = Depends(get_db)):
    return current_user
