from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#JSON consrtuctions
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItem(restaurant_id, menu_id):
    # restaurant = session.query(Restaurant).filter_by(
    #     id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItem=item.serialize)



#Restaurants snd it's modifications
@app.route('/')
@app.route('/restaurants')
def restaurantsList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',
     restaurants=restaurants)


def addNewRestaurant():
    pass

def editRestaurant():
    pass

def delRestaurant():
    pass


#Menu item and modification
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	#restaurants = session.query(Restaurant).all()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	
	return render_template('menu.html', restaurant=restaurant,
		items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods= ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
    	newItem= MenuItem(name= request.form['name'],
    		restaurant_id=restaurant_id)
    	session.add(newItem)
    	session.commit()
        flash("new menu item created!")
    	return redirect(url_for('restaurantMenu',
    		restaurant_id=restaurant_id))
    else:
    	return render_template('new_menu_item.html',
    		restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', 
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Item has been successfully edited!")
        return redirect(url_for('restaurantMenu',
         restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant_id=restaurant_id,
            menu_id=menu_id, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Item has been successfully deleted!")
        return redirect(url_for('restaurantMenu',
         restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html',
            restaurant_id=restaurant_id,
            item = deletedItem)
    




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)