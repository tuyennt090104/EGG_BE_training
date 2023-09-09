from sqlmodel import SQLModel, Field, Relationship

from typing import Optional, List

from datetime import datetime

from enum import Enum


class OrderStatus(Enum):
    init: str = "init"
    done: str = "done"


class CustomerBase(SQLModel):
    name: str
    address: str
    phone: str
    email: str


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orders: List["Order"] = Relationship(back_populates="customer")


class ProductBase(SQLModel):
    name: str
    image: str
    description: str
    price: int
    stock_quantity: int


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_products: List["OrderProduct"] = Relationship(back_populates="product")


class OrderBase(SQLModel):
    customer_id: int = Field(foreign_key="customer.id")
    create_at: datetime
    total_amount: int
    order_status: OrderStatus


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer: Customer = Relationship(back_populates="orders")
    order_products: List["OrderProduct"] = Relationship(back_populates="order")


class OrderProductBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    product_price: int


class OrderProduct(OrderProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product: Product = Relationship(back_populates="order_products")
    order: Order = Relationship(back_populates="order_products")


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int


class OrderUpdate(SQLModel):
    customer_id: Optional[int] = None
    create_at: Optional[datetime] = datetime.now()
    total_amount: Optional[int] = None
    order_status: Optional[OrderStatus] = OrderStatus.init


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    stock_quantity: Optional[int] = None


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductRead(OrderProductBase):
    id: int


class ProductReadWithOderProducts(ProductRead):
    order_products: List[OrderProductRead] = []


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int


class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class CustomerReadWithOrders(CustomerRead):
    orders: List[OrderRead] = []
