# This file defines the classes/tables in database with given fields, datatypes and relationships
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Float, Enum, Date, TypeDecorator, BINARY
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


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


class StaffRole(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, nullable=False, unique=True)
    staff_accounts = relationship("StaffAccount", back_populates="role")


class StaffAccount(Base):
    __tablename__ = 'staff_accounts'
    staff_id = Column(UUID, primary_key=True,
                      default=lambda: uuid.uuid4().bytes)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    gender = Column(Enum('male', 'female', 'others',
                    name='gender'), nullable=False)
    dob = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    role = relationship("StaffRole", back_populates="staff_accounts")
    orders = relationship("Order", back_populates="waiter",
                          primaryjoin="and_(StaffAccount.staff_id == Order.staff_id, StaffAccount.role_id == 1)")
    dishes = relationship("Dish", back_populates="chef",
                          primaryjoin="and_(StaffAccount.staff_id == Dish.staff_id, StaffAccount.role_id == 2)")


class Table(Base):
    __tablename__ = 'tables'
    table_id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer, nullable=False)
    table_status = Column(Enum('vacant', 'reserved', 'eating',
                               name='table_status'), nullable=False, default='vacant')
    orders = relationship("Order", back_populates="table")


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(UUID, primary_key=True,
                      default=lambda: uuid.uuid4().bytes)
    table_id = Column(Integer, ForeignKey('tables.table_id'), nullable=False)
    staff_id = Column(UUID, ForeignKey(
        'staff_accounts.staff_id'), nullable=False)
    is_served = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    table = relationship("Table", back_populates="orders")
    waiter = relationship("StaffAccount", back_populates="orders",
                          primaryjoin="and_(Order.staff_id == StaffAccount.staff_id, StaffAccount.role_id == 1)")
    dishes = relationship("Dish", back_populates="order")


class Dish(Base):
    __tablename__ = 'dishes'
    dish_id = Column(UUID, primary_key=True,
                     default=lambda: uuid.uuid4().bytes)
    order_id = Column(UUID, ForeignKey('orders.order_id'), nullable=False)
    staff_id = Column(UUID, ForeignKey(
        'staff_accounts.staff_id'), nullable=False)
    menu_item_id = Column(UUID, ForeignKey(
        'menu_items.menu_item_id'), nullable=False)
    note = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    dish_status = Column(Enum('received', 'prepared', 'ready',
                              name='dish_status'), nullable=False, default='received')
    order = relationship("Order", back_populates="dishes")
    chef = relationship("StaffAccount", back_populates="dishes",
                        primaryjoin="and_(Dish.staff_id == StaffAccount.staff_id, StaffAccount.role_id == 2)")
    menu_item = relationship("MenuItem", back_populates="dishes")


class MenuItem(Base):
    __tablename__ = 'menu_items'
    menu_item_id = Column(UUID, primary_key=True,
                          default=lambda: uuid.uuid4().bytes)
    menu_section_id = Column(Integer, ForeignKey(
        'menu_sections.menu_section_id'), nullable=False)
    item_name = Column(String, nullable=False, unique=True)
    note = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    dishes = relationship("Dish", back_populates="menu_item")
    menu_section = relationship("MenuSection", back_populates="menu_items")


class MenuSection(Base):
    __tablename__ = 'menu_sections'
    menu_section_id = Column(Integer, primary_key=True, index=True)
    section_name = Column(String, nullable=False)
    menu_items = relationship("MenuItem", back_populates="menu_section")
