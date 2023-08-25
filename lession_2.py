from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: int
    tag: str
    create_at: datetime


engine = create_engine("mysql://root:123456@localhost:3306/egg_gen6", echo=True)


# print(f'engine = {engine}')


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def add(name: str,
        price: int,
        tag: str,
        create_at: datetime):
    product = Product(name=name, price=price, tag=tag, create_at=create_at)
    with Session(engine) as session:
        session.add(product)
        session.commit()


def pop(index: int):
    with Session(engine) as session:
        product = session.get(Product, index)
        if product is not None:
            session.delete(product)
            session.commit()


def count():
    with Session(engine) as session:
        statement = select(Product)
        results = session.exec(statement)
        products = results.all()
        cnt = len(products)
        print(cnt)
    return cnt


def find(name: str):
    with Session(engine) as session:
        statement = select(Product).where(Product.name == name)
        results = session.exec(statement)
        products = results.all()
    return products


def print_all():
    with Session(engine) as session:
        statement = select(Product)


mapping = {
    "name": Product.name,
    "price": Product.price,
    "tag": Product.tag,
    "create_at": Product.create_at
}


def get_all(limit: int, offset: int, order_by: str):
    [column, order] = order_by.split('-')
    with Session(engine) as session:
        if order == "asc":
            statement = select(Product).order_by(mapping[column].asc()).offset(offset).limit(limit)
        if order == "desc":
            statement = select(Product).order_by(mapping[column].desc()).offset(offset).limit(limit)
        result = session.exec(statement)
        products = result.all()
    return products


def upd(index: int, schema: dict):
    with Session(engine) as session:
        product = session.get(Product, index)
        product.name = schema["name"]
        product.price = schema["price"]
        product.tag = schema["tag"]
        product.create_at = schema["create_at"]
        session.add(product)
        session.commit()


def main():
    create_db_and_tables()
    count()
    add(name="Beef", price=1, tag="Food", create_at=datetime.now())
    # pop(index=1)
    count()
    upd(index=1, schema={"name": "Coca", "price": 3, "tag": "Drink", "create_at": datetime.now()})
    print(find("Beef"))
    print(get_all(3, 0, "price-asc"))


if __name__ == "__main__":
    main()