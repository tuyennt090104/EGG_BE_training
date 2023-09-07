from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime


class Status(Enum):
    init = "init"
    done = "done"


class CustomerBase(SQLModel):
    name: str
    address: str
    phone: str
    email: str


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orders: List["Order"] = Relationship(back_populates="customer")


class CustomerRead(CustomerBase):
    id: int


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class ProductBase(SQLModel):
    name: str
    image: str
    description: str
    price: int
    stock_quantity: int


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_products: List["OrderProduct"] = Relationship(back_populates="product")


class ProductRead(ProductBase):
    id: int


class ProductReadCompact(SQLModel):
    id: int
    name: str
    image: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    stock_quantity: Optional[int] = None


class OrderBase(SQLModel):
    customer_id: int = Field(foreign_key="customer.id")
    create_at: datetime
    total_amount: int
    order_status: Status


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer: Customer = Relationship(back_populates="orders")
    order_products: List["OrderProduct"] = Relationship(back_populates="order")


class OrderCreate(OrderBase):
    create_at: Optional[datetime] = None
    order_status: Optional[Status] = Status.init


class OrderRead(OrderBase):
    id: int


class OrderReadCompact(SQLModel):
    create_at: datetime
    total_amount: int
    order_status: Status


class OrderProductBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    product_price: int


class OrderProduct(OrderProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order: Order = Relationship(back_populates="order_products")
    product: Product = Relationship(back_populates="order_products")


class OrderProductRead(OrderProductBase):
    id: int


class ProductReadWithOrderProducts(ProductRead):
    order_products: List[OrderProductRead] = []


class CustomerReadWithOrders(CustomerRead):
    orders: List[OrderReadCompact] = []
