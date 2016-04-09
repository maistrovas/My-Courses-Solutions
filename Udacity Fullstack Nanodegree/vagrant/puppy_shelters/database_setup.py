import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import select, func

Base = declarative_base()



class Shelter(Base):
	__tablename__ = 'shelter'

	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)
	address = Column(String(250))
	city = Column(String(50))
	state = Column(String(50))
	zipCode = Column(String(10))
	website = Column(String(50))
	maximum_capacity = Column(Integer, default = 50)
	current_occupancy = Column(Integer)
	
class Puppy(Base):
	__tablename__ = 'puppy'

	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)
	dateOfBirth = Column(Date)
	picture = Column(String)
	gender = Column(String(50))
	weight = Column(Numeric(10))
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	#Case One-To-One relationship
	#profiles = relationship('Puppy_profile', uselist=False, back_populates="puppy")

#Association table for Many-To-Many relationship
association_table = Table('association', Base.metadata,
	Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Puppy_profile(Base):
	__tablename__ = 'left'
	#Case one-to-one
	#puppy_id = Column(Integer, ForeignKey('puppy.id'))
	#puppy = relationship('Puppy', back_populates = "puppy_profile")
	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)
	dateOfBirth = Column(Date)
	picture = Column(String)
	gender = Column(String(50))
	weight = Column(Numeric(10))
	description = Column(String(500))
	url = Column(String(50))
	special_needs = Column(String(500))
	
	adopters = relationship("Adopters", 
		secondary=association_table,
		back_populates = "puppy_profile")

class Adopters(Base):
    __tablename__ = 'right'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    adress = Column(String(150))
    #puppy_id = Column(Integer, ForeignKey('puppy_profile'))
    puppy_profile = relationship("Puppy_profile", secondary=association_table, back_populates="adopters")


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)

