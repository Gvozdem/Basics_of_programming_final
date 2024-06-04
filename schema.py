import datetime as dt

# Импортируем из библитеки SqlAlchemy нужные функции и классы
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy import Integer, String, Boolean, DateTime, Numeric, SmallInteger

# Импортируем из подмодуля ORM функции и классы, предназначенные для
# высокоуровневой работы с базой данных посредством построения объектной модели ORM
# (ORM ~ object-relational model)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


# Так просто надо сделать
class Basis(DeclarativeBase):
    pass


class User(Basis):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(50))
    created_on = Column(DateTime(), default=dt.datetime.now)
    updated_on = Column(DateTime(), default=dt.datetime.now, onupdate=dt.datetime.now)
    
    sent_messages = relationship("Message", foreign_keys="[Message.author_id]", back_populates="author")
    received_messages = relationship("Message", foreign_keys="[Message.recipient_id]", back_populates="recipient")
    cookies = relationship("Cookie", back_populates="user")

    def __str__(self):
        return f"<{self.id}> {self.first_name} {self.last_name} aka {self.username}"

    def __repr__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"



class Message(Basis):
    __tablename__ = "messages"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False, default="(без темы)")
    content = Column(String())
    author_id = Column(Integer(), ForeignKey('users.id'))
    recipient_id = Column(Integer(), ForeignKey('users.id'))
    is_private = Column(Boolean(), default=True, nullable=False)
    created_on = Column(DateTime(), default=dt.datetime.now)
    updated_on = Column(DateTime(), default=None, onupdate=dt.datetime.now)

    author = relationship("User", foreign_keys="[Message.author_id]", back_populates="sent_messages")
    recipient = relationship("User", foreign_keys="[Message.recipient_id]", back_populates="received_messages")

    def __str__(self):
        return f"<{self.id}> {self.title}: {self.content[:20]}"

    def __repr__(self):
        return f"<{self.id}> {self.title}"


class Cookie(Basis):
    __tablename__ = "cookie"
    cookie = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey('users.id'))

    user = relationship("User", back_populates="cookies")


engine = create_engine("sqlite:///My Database/blog.db?echo=True")

Basis.metadata.create_all(engine)

factory = sessionmaker(bind=engine)
