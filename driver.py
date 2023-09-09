from sqlmodel import create_engine, SQLModel, Session


class Driver:
    def __init__(self):
        self.engine = create_engine("mysql://root:123456@localhost/mydb", echo=True)
        print(f'engine:{self.engine}')

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def make_session(self):
        return Session(self.engine)
