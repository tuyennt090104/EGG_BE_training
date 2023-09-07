from sqlmodel import create_engine, SQLModel

engine = create_engine("mysql://root:123456@localhost/egg_gen6", echo=True)
print(f'engine:{engine}')


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

