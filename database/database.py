import datetime
from sqlalchemy import Column, Integer, String, create_engine, DECIMAL, ForeignKey, \
    DateTime, Boolean, exists, Date
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

    def __repr__(self):
        return f"{self.user_id} {self.fio}"

    @staticmethod
    def check_user_exists(user_id):
        query = session.query(exists().where(User.user_id == user_id)) \
            .scalar()
        return query

    @staticmethod
    def get_users():
        query = session.query(User.user_id, User.fio, User.phone_number, User.is_active).all()
        return query

    @staticmethod
    def get_user(user_id):
        query = session.query(User.fio, User.phone_number)\
            .filter(User.user_id == user_id)\
            .all()[0]
        return query

    @staticmethod
    def check_user_is_active(user_id):
        query = session.query(exists().where(User.user_id == user_id) \
                              .where(User.is_active == True)) \
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
        return True


class Template(base):
    __tablename__ = 'Template'
    id = Column(Integer, primary_key=True)
    template_name = Column(String)
    is_active = Column(Boolean)
    date_update = Column(Date, default=datetime.date.today())
    category = relationship("Category", cascade="delete")

    def __repr__(self):
        return self.template_name

    @staticmethod
    def drop_template(template_id):
        session.query(Template).filter(Template.id == template_id).delete()
        session.commit()

    @staticmethod
    def get_template_id(template_name):
        query = session.query(Template.id)\
            .filter(Template.template_name == template_name)\
            .all()[0].id
        return query

    @staticmethod
    def get_templates():
        query = session.query(Template.template_name).all()
        return query

    @staticmethod
    def set_false():
        session.query(Template).filter(Template.is_active == True) \
            .filter(Template.date_update == datetime.date.today())\
            .update({"is_active": False})
        session.commit()

    @staticmethod
    def get_menu_status():
        today = datetime.date.today()
        query = session.query(Template.is_active)\
                .filter(Template.date_update == today)\
                .all()
        for template in query:
            if template.is_active:
                return "Меню активно"
        for template in query:
            if template.is_active is False:
                return "Меню не активно"
        return "Меню не выставлено"


class Category(base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    template = Column('template', Integer, ForeignKey("Template.id"))
    dish = relationship("Dish", cascade="delete")

    def __repr__(self):
        return f"{self.id} {self.category_name} {self.dish}"

    @staticmethod
    def add_category(category_name, template_id):
        category = Category(category_name=category_name, template=template_id)
        session.add(category)
        session.commit()

    @staticmethod
    def get_catygoryes(template=session.query(Template.id).filter(Template.is_active == True)\
                       .filter(Template.date_update == datetime.date.today())
                       .all()[0].id):
        if template:
            query = session.query(Category).filter(Category.template == template).all()
            return query


class Dish(base):
    __tablename__ = 'Dish'
    id = Column(Integer, primary_key=True)
    dish_name = Column(String)
    dish_description = Column(String)
    dish_price = Column(DECIMAL)
    dish_photo = Column(String)
    category = Column(Integer, ForeignKey("Category.id"))

    def __repr__(self):
        return f"{self.dish_name} {self.category}"

    @staticmethod
    def get_dishes(category):
        query = session.query(Dish.dish_name, Dish.dish_description,
                              Dish.dish_price, Dish.dish_photo, Category.category_name) \
                            .join(Category) \
                            .filter(Category.category_name == category)\
                            .all()
        return query


class OrderList(base):
    __tablename__ = 'OrderList'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_phone_number = Column(String)
    user_id = Column(Integer)
    dish_name = Column(String)
    dish_price = Column(DECIMAL)
    date_create = Column(Date)
    is_active = Column(Boolean)

    def __repr__(self):
        return f"{self.user_id} {self.user_name} {self.dish_name} {self.date_create}"

    @staticmethod
    def get_orders():
        query = session.query(
            OrderList.user_id,
            OrderList.user_name,
            OrderList.user_phone_number,
            OrderList.dish_name,
            OrderList.dish_price,
        ).order_by(OrderList.user_name) \
            .filter(OrderList.date_create == datetime.date.today()) \
            .filter(OrderList.is_active == True)\
            .all()
        return query

    @staticmethod
    def drop_order(user_id, dish_name):
        session.query(OrderList).filter(OrderList.user_id == user_id)\
                                .filter(OrderList.dish_name == dish_name)\
                                .update({"is_active": False})
        session.commit()

    @staticmethod
    def get_order_today(user_id):
        query = session.query(OrderList.dish_name, OrderList.dish_price) \
            .filter(OrderList.user_id == user_id) \
            .filter(OrderList.date_create == datetime.date.today()) \
            .all()
        return query

    @staticmethod
    def check_order_today(user_id):
        query = session.query(exists().where(OrderList.user_id == user_id) \
                              .where(OrderList.date_create == datetime.date.today())) \
            .scalar()
        return query

    @staticmethod
    def accept_order(data_set: set, user_id):
        user = session.query(User.fio, User.phone_number) \
            .filter(User.user_id == user_id) \
            .all()
        dishes_price = session.query(Dish.dish_name, Dish.dish_price) \
            .filter(Dish.dish_name.in_(data_set)) \
            .all()
        for query in dishes_price:
            order = OrderList(
                user_name=user[0].fio,
                user_phone_number=user[0].phone_number,
                user_id=user_id,
                dish_name=query.dish_name,
                dish_price=query.dish_price,
                date_create=datetime.date.today(),
                is_active=True
            )
            session.add(order)
        session.commit()


if __name__ == "__main__":
    base.metadata.create_all(engine)
