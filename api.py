from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

from repository import IRepository, SqlmodelRepository

from models import *

app: FastAPI = FastAPI()
repo: IRepository = SqlmodelRepository()


def get_session():
    with repo.make_session() as session:
        yield session


@app.post("/products/", response_model=ProductRead)
async def create_product(*, session: Session = Depends(get_session), product: ProductCreate):
    return repo.create_product(session, product)


@app.get("/products/", response_model=List[ProductRead])
async def get_all_products(*, session: Session = Depends(get_session)):
    return repo.get_all_products(session)


@app.get("/products/{id}", response_model=ProductReadWithOderProducts)
async def get_detail_product(*, session: Session = Depends(get_session), id: int):
    product = repo.get_by_id_product(session, id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@app.patch("/products/{id}", response_model=ProductRead)
async def update_product(*, session: Session = Depends(get_session), id: int, product: ProductUpdate):
    updated_product = repo.update_by_id_product(session, id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="product not found")
    return updated_product


@app.delete("/products/{id}")
async def delete_product(*, session: Session = Depends(get_session), id: int):
    if repo.delete_by_id_product(session, id):
        return {"ok": True}
    raise HTTPException(status_code=404, detail="product not found")


@app.post("/customers/", response_model=CustomerRead)
async def create_customer(*, session: Session = Depends(get_session), customer: CustomerCreate):
    return repo.create_customer(session, customer)


@app.get("/customers/", response_model=List[CustomerRead])
def get_all_customers(*, session: Session = Depends(get_session)):
    return repo.get_all_customers(session)


@app.get("/customers/{id}", response_model=CustomerReadWithOrders)
def get_detail_customer(*, session: Session = Depends(get_session), id: int):
    customer = repo.get_by_id_customer(session, id)
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")
    return customer


@app.patch("/customers/{id}", response_model=CustomerRead)
def update_customer(*, session: Session = Depends(get_session), id: int, customer: CustomerUpdate):
    updated_customer = repo.update_by_id_customer(session, id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="customer not found")
    return updated_customer


@app.delete("/customers/{id}")
def delete_customer(*, session: Session = Depends(get_session), id: int):
    if repo.delete_by_id_customer(session, id):
        return {"ok": True}
    raise HTTPException(status_code=404, detail="customer not found")


@app.post("/orders/", response_model=OrderRead)
def create_order(*, session: Session = Depends(get_session), order: OrderCreate):
    return repo.create_order(session, order)


@app.patch("/orders/{id}", response_model=OrderRead)
def convert_status_order(*, session: Session = Depends(get_session), id: int):
    order = OrderUpdate.parse_obj({"order_status": OrderStatus.done})
    return repo.update_by_id_order(session, id, order)
