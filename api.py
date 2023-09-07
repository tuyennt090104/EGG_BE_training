from typing import Dict, List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import *
from driver import create_db_and_tables, engine

app = FastAPI()


async def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.post("/products/", response_model=ProductRead)
async def create_product(*, session: Session = Depends(get_session), product: ProductCreate):
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[ProductReadCompact])
async def get_all_products(*, session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products


@app.get("/products/{index}", response_model=ProductReadWithOrderProducts)
async def get_detail_product(*, session: Session = Depends(get_session), index: int):
    product = session.get(Product, index)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.patch("/products/{index}", response_model=ProductRead)
async def update_product(*, session: Session = Depends(get_session), index: int, product: ProductUpdate):
    db_product = session.get(Product, index)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.delete("/products/{index}")
async def delete_product(*, session: Session = Depends(get_session), index: int):
    product = session.get(Product, index)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"oke": True}


@app.post("/customers/", response_model=CustomerRead)
async def create_customer(*, session: Session = Depends(get_session), customer: CustomerCreate):
    db_customer = Customer.from_orm(customer)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


@app.get("/customers/", response_model=List[CustomerRead])
async def get_all_customers(*, session: Session = Depends(get_session)):
    customers = session.exec(select(Customer)).all()
    return customers


@app.get("/customers/{index}", response_model=CustomerReadWithOrders)
async def get_detail_customer(*, session: Session = Depends(get_session), index: int):
    customer = session.get(Customer, index)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.patch("/customers/{index}", response_model=CustomerRead)
async def update_customer(*, session: Session = Depends(get_session), index: int, customer: CustomerUpdate):
    db_customer = session.get(Customer, index)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_data = customer.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


@app.delete("/customers/{index}")
async def delete_customer(*, session: Session = Depends(get_session), index: int):
    customer = session.get(Customer, index)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"Ok": True}


@app.post("/orders/", response_model=OrderRead)
async def create_order(*, session: Session = Depends(get_session), order: OrderCreate):
    if not order.create_at:
        order.create_at = datetime.now()
    db_order = Order.from_orm(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@app.patch("/orders/{index}", response_model=OrderRead)
async def convert_status(*, session: Session = Depends(get_session), index: int):
    order = session.get(Order, index)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_status = Status.done
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
