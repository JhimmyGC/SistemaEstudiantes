from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB:
    engine = create_engine(
        "postgresql://postgres:admin@localhost:5432/sistemaestudiantes"
    )
    Session = sessionmaker(bind=engine)

    @classmethod
    def conectar(cls):
        return cls.Session()
