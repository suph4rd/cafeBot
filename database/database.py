import datetime

from sqlalchemy import Column, Integer, String, create_engine, DECIMAL, ForeignKey, DateTime, Boolean, Table, exists
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# postgresql://example:example@localhost:5432/example
from config import DB_USER, DB_PASSWORD, DB_DOMAIN, DB_PORT, DB_NAME

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_DOMAIN}:{DB_PORT}/{DB_NAME}")
base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    fio = Column(String)
    date_create = Column(DateTime)
    is_active = Column(Boolean)
    phone_number = Column(String)

    @staticmethod
    def check_user_exists(user_id):
        query = session.query(exists().where(User.user_id == user_id))\
                                        .scalar()
        return query

    @staticmethod
    def check_user_is_active(user_id):
        query = session.query(exists().where(User.user_id == user_id)\
                                        .where(User.is_active == True))\
                                        .scalar()
        return query

    @staticmethod
    def create_user(user: dict):
        new_user = User(
            user_id=user.get("user_id"),
            fio=user.get("fio"),
            phone_number=user.get("phone_number"),
            date_create=datetime.datetime.now(),
            is_active=True
        )
        session.add(new_user)
        session.commit()

    @staticmethod
    def update_user(user_dict: dict):
        user_id = user_dict.get("user_id")
        session.query(User).filter(User.user_id == user_id).update(user_dict)
        session.commit()


template_category_m2m = Table('template_category_m2m',
                            base.metadata,
                            Column('template_id', Integer, ForeignKey("Template.id")),
                            Column('category_id', Integer, ForeignKey("Category.id"))
                              )


class Template(base):
    __tablename__ = 'Template'
    id = Column(Integer, primary_key=True)
    template_name = Column(String)
    is_active = Column(Boolean)


dish_category_m2m = Table('dish_category_m2m',
                            base.metadata,
                            Column('dish_id', Integer, ForeignKey("Dish.id")),
                            Column('category_id', Integer, ForeignKey("Category.id"))
                              )


class Category(base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    template = relationship(
        "Template",
        secondary=template_category_m2m,
        backref="parents"
    )

    @staticmethod
    def get_catygoryes():
        query = session.query(Category).all()
        return query


class Dish(base):
    __tablename__ = 'Dish'
    id = Column(Integer, primary_key=True)
    dish_name = Column(String)
    dish_description = Column(String)
    dish_price = Column(DECIMAL)
    dish_photo = Column(String)
    category = relationship(
        "Category",
        secondary=dish_category_m2m,
        backref="parents"
    )

    @staticmethod
    def get_dishes(category="первое"):
        query = session.query(Dish.dish_name, Dish.dish_description,
                              Dish.dish_price, Dish.dish_photo,
                              Category.category_name)\
            .join(Category, Dish.category)\
            .filter(Category.category_name==category).all()
        return query


class OrderList(base):
    __tablename__ = 'OrderList'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_phone_number = Column(String)
    user_id = Column(Integer)
    dish_name = Column(String)
    dish_price = Column(DECIMAL)
    date_create = Column(DateTime)
    is_active = Column(Boolean)


if __name__ == "__main__":
    base.metadata.create_all(engine)