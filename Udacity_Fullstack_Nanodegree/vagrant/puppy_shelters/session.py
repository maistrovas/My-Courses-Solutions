import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Shelter, Base,  Puppy
from sqlalchemy import func
engine = create_engine('sqlite:///puppyshelter.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Query 1
'''
papy = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
for i in papy:
	print i.name
'''

#Query 2
'''
today = datetime.date.today()
half_year = datetime.timedelta(days=180)
six_month_before = today - half_year

yang_papy = session.query(Puppy).filter(
	Puppy.dateOfBirth > six_month_before).order_by(
	Puppy.dateOfBirth.desc()).all()
for i in yang_papy:
	print 'Pappy named %s born date is %s' %(i.name, i.dateOfBirth)
'''


#Query 3
'''
pappy_weight = session.query(Puppy).order_by(Puppy.weight.asc()).all()

for i in  pappy_weight:
	print i.name, i.weight
'''

#Query 4
grouped_puppy = session.query(Shelter.name, func.count(Puppy.name)).filter(Shelter.id == Puppy.shelter_id).group_by(Puppy.shelter_id).all()
#print grouped_puppy
#w = 0
#for i in grouped_puppy:
#	print  i


###EX - 5
capacity = session.query(Shelter.name, Shelter.maximum_capacity).all()

#for i in capacity:
#	print i
def check_is_spaces(capacity, papys_in_shelters, pappy):
	'''
	capacity - is list with elementsc like (shelter_name, max_spaces)
	papys_in_shelters - is list with elements like (shelter_name, amount_pupies)
	pappy - integer, amount of pappies that qant to be added
	in shelter.
	return:
	dict with name of shelter and number of free
	spaces inside.
	
	'''
	shelters_spaces = {}
	for i in range(len(papys_in_shelters)):
		shelters_spaces[papys_in_shelters[i][0]] = capacity[i][1] - papys_in_shelters[i][1]
	places = 50
	recomended_shelter = []
	for shelter in shelters_spaces:
		if shelters_spaces[shelter] + pappy  < places:
			recomended_shelter.append(shelter)
	if len(recomended_shelter) > 0:
		print 'Here is the name of a shelter with free spaces', random.choice(recomended_shelter)
	else:
		print  'Sorry aur shelters are full ! Please try later.'

check_is_spaces(capacity, grouped_puppy, 20)



