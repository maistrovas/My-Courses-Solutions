from flask import Flask, render_template,url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Restaurant, MenuItem, Base, User
###Imports for OAuth2 Course
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests



engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



app = Flask(__name__)

@app.route('/login')
def showLogin():
	state = ''.join(random.choice( \
		string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id'] 

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    ##Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    #data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if user_id == None:
    	user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    for i in login_session:
        print i
        print login_session[i]
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s' %(access_token)
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %(login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
    	print 'result status =', result['status'] 
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response



@app.route('/fbconnect', methods=['POST'])
def fbconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'),401)
		response.headers['Content-Type'] = 'application/json'
		return response
	access_token = request.data





##API Endpoints
@app.route('/restaurants/JSON/')
def showRestaurantsJson():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants=[rest.serialize for rest in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def showMenuJson(restaurant_id):
	items = session.query(MenuItem).filter_by(
		restaurant_id=restaurant_id).all()
	return jsonify(Menu_Items= [item.serialize for item in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJson(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(Item = [item.serialize] )

##Pages routes
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	if 'username' not in login_session:
		return render_template('publicrestaurants.html',
			restaurants=restaurants)
	else:
	    return render_template('restaurants.html',
	    	restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newItem = Restaurant(name=request.form['name'],
			user_id = login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash("New restaurant has been sucksessfully added!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	if 'username' not in login_session:
		
		return redirect('/login')

	editedRestaurant = session.query(Restaurant).filter_by(
		id = restaurant_id).one()
	creator = getUserInfo(editedRestaurant.user_id)
	if login_session['email'] !=  creator.email:
		return '<script>function alertFunc() {alert("You are not authorized\
		 to edit this restaurant. Please create your own one in order to\
		 do it.");}</script> <body onload="alertFunc()">'


	
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant has been sucksessfully edited!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant_id = restaurant_id,
		restaurant = editedRestaurant )

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	if 'username' not in login_session:
		return redirect('/login')
	deletedRestaurant = session.query(Restaurant).filter_by(
		id=restaurant_id).one()
	creator = getUserInfo(deletedRestaurant.user_id)
	if login_session['email'] !=  creator.email:
		return '<script>function alertFunc() {alert("You are not authorized\
		 to delete this restaurant. Please create your own one in order to\
		 do it.");}</script> <body onload="alertFunc()">'
	if request.method =='POST':
		session.delete(deletedRestaurant)
		session.commit()
		flash("Restaurant has been sucksessfully deleted!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant_id=restaurant_id,
			restaurant = deletedRestaurant)



@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	items = session.query(MenuItem).filter_by(
		restaurant_id=restaurant_id).order_by(MenuItem.course).all()
	restaurant= session.query(Restaurant).filter_by(
		id=restaurant_id).one()
	courses = session.query(MenuItem.course).filter_by(
		restaurant_id=restaurant_id).order_by(MenuItem.course).distinct().all()
	
	creator = getUserInfo(restaurant.user_id)
	creator_email = creator.email
	print 'Page creator_ID=',creator.id
	print 'Creator email =',creator.email
	print "Creator name =", creator.name
	print "Creator pict =", creator.picture
	try:
		print 'Logged person name =', login_session['username']
		print 'Logged person email =',login_session['email']
		logged_person_email = login_session['email']
		permission = logged_person_email == creator_email
	except:
		print 'No User logged in'
	if permission:
		print 'Rendering major page'
		return render_template('menu.html', restaurant_id=restaurant_id,
			items=items,
			restaurant=restaurant,
			courses=courses,
			creator=creator)
	else:
		print 'Rendering public page'
		return render_template('publicmenu.html', restaurant_id=restaurant_id,
			items=items,
			restaurant=restaurant,
			courses=courses,
			creator=creator)




@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if 'username' not in login_session:
		return redirect('/login')
	restaurant = session.query(Restaurant).filter_by(
		id=restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],
		description = request.form['description'],
		price = request.form['price'],
		course = request.form['course'],
		restaurant=restaurant,
		user_id = login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash("New item has been sucksessfully added!")
		return redirect(url_for('showMenu',
		 restaurant_id=restaurant_id))
	else:	
		return render_template('newMenuItem.html',
			restaurant_id=restaurant_id,
			restaurant=restaurant )

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	if 'username' not in login_session:
		return redirect('/login')
	editedItem = session.query(MenuItem).filter_by(
		id=menu_id).one()
	creator = getUserInfo(editedItem.user_id)
	if login_session['email'] !=  creator.email:
		return '<script>function alertFunc() {alert("You are not authorized\
		 to edit this item. Please create your own one in order to\
		 do it.");}</script> <body onload="alertFunc()">'

	if request.method == 'POST':
		if len(request.form['name']) > 3:
			editedItem.name = request.form['name']
		else:
			editedItem.name = editedItem.name
		if len(request.form ['description']) > 5:
			editedItem.description = request.form['description']
		else:
			editedItem.description = editedItem.description
		if len(request.form['price']) > 1:
			editedItem.price = request.form['price']
		else:
			editedItem.price = editedItem.price
		if len(request.form['course']) > 3:
			editedItem.course = request.form['course']
		else:
			editedItem.course = editedItem.course
		session.add(editedItem)
		session.commit()
		flash("Item has been sucksessfully edited!")
		return redirect(url_for('showMenu',
		    restaurant_id= restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id=restaurant_id,
			item=editedItem )

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	if 'username' not in login_session:
		return redirect('/login')
	deletedItem = session.query(MenuItem).filter_by(
		id=menu_id).one()
	creator = getUserInfo(deletedItem.user_id)
	if login_session['email'] !=  creator.email:
		return '<script>function alertFunc() {alert("You are not authorized\
		 to delete this item. Please create your own one in order to\
		 do it.");}</script> <body onload="alertFunc()">'

	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Item has been sucksessfully deleted!")
		return redirect(url_for('showMenu',
		 restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id=restaurant_id,
			item = deletedItem)

def createUser(login_session):
	'''
	returns user_id new created user
	'''
	newUser = User(name= login_session['username'],
			email = login_session['email'],
			picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email= login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	'''
	returns user object assocciated with user_id
	'''
	user = session.query(User).filter_by(id = user_id).one()
	return user

def getUserID(email):
	'''
	return id that belog to email if it exist
	'''
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None


if __name__ == '__main__':
	app.secret_key = '1111'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)