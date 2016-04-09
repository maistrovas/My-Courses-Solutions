from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

#Creating a session and connecting to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()




def get_restaurants():
    '''
    function retrieve restaurant list fom DB
    '''
    rest = session.query(Restaurant.name).all()
    return rest



def add_restaurant(item_name):
    '''
    adds new restaurant to the DB
    item_name - string of name
    '''
    new_restaurant = Restaurant(name=item_name) 
    session.add(new_restaurant)
    session.commit()
    new_restaurants = session.query(Restaurant.name).all()
    return new_restaurants

def update_restaurant_name(item_name, new_name):
    '''
    item_name - str. with name of item that should be changed
    new_name - str. with new name of item
    '''
    item = session.query(Restaurant).filter_by(name = item_name).one()
    item.name = new_name
    session.add(item)
    session.commit()

def delete_restaurant_name(item_name):
    '''
    item_name - str. name of restaurant being deleted
    '''
    item = session.query(Restaurant).filter_by(name = item_name).one()
    session.delete(item)
    session.commit()

def cleann_empty():
    '''
    deletes all names thar was empty string
    '''
    items = ession.query(Restaurant).filter_by(name = '').all()
    for item in items:
        session.delete(item)
        session.commit()

class ServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1> Make a New Restaurant</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><input name='restaurant' type='text'> <input type='submit' value='Create'> </form>"
            output += "</html></body>"
            self.wfile.write(output)
            #print output
            return

        # Restaurants are available via indexes
        # in list of restaurants     
        for ind in range(len(get_restaurants())):
            if self.path.endswith("/restaurants/%s/edit" % ind):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>%s<h2>" % get_restaurants()[ind].name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><input name='%s/edit' type='text' placeholder ='%s'> <input type='submit' value='Rename'> </form>" % (ind,get_restaurants()[ind].name)
                output += "</html></body>"
                self.wfile.write(output)
                #print output
                return
    
            if self.path.endswith("/restaurants/%s/delete" % ind):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Do you sure you want to delete ?<h1>"
                output += "<h1>%s<h1>" % get_restaurants()[ind].name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'> <input name='%s/delete' type='submit' value='Delete'> </form>" % ind
                output += "</html></body>"
                self.wfile.write(output)
                #print output
                return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            output = ""
            output += "<html><body>"
            for ind in range(len(get_restaurants())):
                output += "<h3> %s  <br><a href='/restaurants/%s/edit'> Edit </a> <br> <a href='/restaurants/%s/delete'> Delete </a> </h3>"  % (get_restaurants()[ind].name, ind, ind)  
            output += "<h2><a href='/restaurants/new'> Make a New Restaurant Here </a></h2>"
            output += "</html></body>"
            self.wfile.write(output)
            #print output
            return

        
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    



    def do_POST(self):

        try:
            #extracting information from the form
            ctype, pdict = cgi.parse_header(self.headers.getheader(
                'content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                for elem in fields:
                    messagecontent = fields.get('%s' % elem) 
                #Uses name of form as input
                    option = fields.keys()[0]
                    print 'Option=', option
            print "Restaurant =", option == 'restaurant'
            
            if option == 'restaurant':
                rest = add_restaurant(messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            
            #Case when we are edit data 
            for ind in range(len(get_restaurants())):
                if option  == '%s/edit' % ind:
                    print "Updated name = ", get_restaurants()[ind].name
                    print "New Name =", messagecontent[0]
                    update_restaurant_name(get_restaurants()[ind].name, messagecontent[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
    
                if option  == '%s/delete' % ind:
                    delete_restaurant_name(get_restaurants()[ind].name)
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            


        except:
            pass

def main():
    try:
        port = 8000
        server = HTTPServer(('', port), ServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()
if __name__ == '__main__':
    main()