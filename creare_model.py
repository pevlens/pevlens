from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, create_engine, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import column
from datetime import datetime
from config import PG_USER, host, PG_PASS

Base = declarative_base()

engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@{host}:5432/test")

class User(Base):

    __tablename__ = 'users'
    __tableargs__ = {
        'comment': 'полтьзователи'
    }

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    username = Column(String(128), comment='Имя пользователя')
    full_name = Column(Text, comment='полное имя')
    chat_id = Column(
        Integer,
        nullable=False,
        unique=True,
        
    )
    reveral = Column(Integer)
    balance = Column(Integer, default=0)
    time_update = Column(DateTime(), onupdate=datetime.now, default=datetime.now ,comment='Дата и обновления')

    def __repr__(self):
        return f'{self.chat_id} {self.username} {self.full_name} {self.reveral} {self.balance}'



Base.metadata.create_all(engine)
