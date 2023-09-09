from abc import ABC, abstractmethod

from sqlmodel import Session, select

from driver import Driver
from models import *


class IRepository(ABC):
    driver: Driver

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def make_session(self):
        raise NotImplementedError

    @abstractmethod
    def create_product(self, session: Session, product: ProductCreate):
        raise NotImplementedError

    @abstractmethod
    def get_all_products(self, session: Session):
        raise NotImplementedError

    @abstractmethod
    def get_by_id_product(self, session: Session, id: int):
        raise NotImplementedError

    @abstractmethod
    def update_by_id_product(self, session: Session, id: int, product: ProductUpdate):
        raise NotImplementedError

    @abstractmethod
    def delete_by_id_product(self, session: Session, id: int):
        raise NotImplementedError

    @abstractmethod
    def create_customer(self, session: Session, customer: CustomerCreate):
        raise NotImplementedError

    @abstractmethod
    def get_all_customers(self, session: Session):
        raise NotImplementedError

    def get_by_id_customer(self, session: Session, id: int):
        raise NotImplementedError

    def update_by_id_customer(self, session: Session, id: int, customer: CustomerUpdate):
        raise NotImplementedError

    def delete_by_id_customer(self, session: Session, id: int):
        raise NotImplementedError

    def create_order(self, session: Session, order: OrderCreate):
        raise NotImplementedError

    def update_by_id_order(self, session: Session, id: int, order: OrderUpdate):
        raise NotImplementedError


class SqlmodelRepository(IRepository):
    def __init__(self):
        self.driver = Driver()
        self.driver.create_db_and_tables()

    def make_session(self):
        return self.driver.make_session()

    def create_product(self, session: Session, product: ProductCreate):
        db_product = Product.from_orm(product)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product

    def get_all_products(self, session: Session):
        products = session.exec(select(Product)).all()
        return products

    def get_by_id_product(self, session: Session, id: int):
        product = session.get(Product, id)
        return product

    def update_by_id_product(self, session: Session, id: int, product: ProductUpdate):
        db_product = session.get(Product, id)
        if not db_product:
            return db_product
        product_data = product.dict(exclude_unset=True)
        for key, value in product_data.items():
            setattr(db_product, key, value)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product

    def delete_by_id_product(self, session: Session, id: int):
        product = session.get(Product, id)
        if not product:
            return False
        session.delete(product)
        session.commit()
        return True

    def create_customer(self, session: Session, customer: CustomerCreate):
        db_customer = Customer.from_orm(customer)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

    def get_all_customers(self, session: Session):
        customers = session.exec(select(Customer)).all()
        return customers

    def get_by_id_customer(self, session: Session, id: int):
        customer = session.get(Customer, id)
        return customer

    def update_by_id_customer(self, session: Session, id: int, customer: CustomerUpdate):
        db_customer = session.get(Customer, id)
        if not db_customer:
            return db_customer
        customer_data = customer.dict(exclude_unset=True)
        for key, value in customer_data.items():
            setattr(db_customer, key, value)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

    def delete_by_id_customer(self, session: Session, id: int):
        customer = session.get(Customer, id)
        if not customer:
            return False
        session.delete(customer)
        session.commit()
        return True

    def create_order(self, session: Session, order: OrderCreate):
        db_order = Order.from_orm(order)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

    def update_by_id_order(self, session: Session, id: int, order: OrderUpdate):
        db_order = session.get(Order, id)
        if not db_order:
            return db_order
        order_data = order.dict(exclude_unset=True)
        for key, value in order_data.items():
            setattr(db_order, key, value)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
