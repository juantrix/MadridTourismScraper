from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///db/database.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class BaseModel:
    def __str__(self):
        return str(self.id)


class Category(Base, BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='empty')
    description = Column(String)
    image = Column(String)
    routes = relationship('Route', back_populates='category')


class Route(Base, BaseModel):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String)
    description = Column(String)
    image = Column(String)
    category = relationship('Category', back_populates='routes')
    itineraries = relationship('Itinerary', back_populates='route')


class Itinerary(Base, BaseModel):
    __tablename__ = 'itinerary'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    name = Column(String)
    description = Column(String, default='None')
    image = Column(String)
    route = relationship('Route', back_populates='itineraries')
    steps = relationship('Step', back_populates='itinerary')


class Step(Base, BaseModel):
    __tablename__ = 'step'

    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itinerary.id'))
    name = Column(String)
    description = Column(String, default='None')
    image = Column(String)
    itinerary = relationship('Itinerary', back_populates='steps')


Base.metadata.create_all(engine)
