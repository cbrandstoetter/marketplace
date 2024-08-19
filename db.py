import sqlite3
"""
this fle contains the sql queries
interaction with the database will be exclusively handled here for better security and overview and easier debugging
keys are in general designed in a that shadow the correspoding columns in sql. this makes dynamic data insertion possible --> new listing()
apart from dynamic data insertion, static insertion is also used as an example --> listing_by_id()
in general, data will be returned as dictionary if possible for easy and streamlined access
"""

def listing_by_id(id):
# provide the id and get the corresponding listing information as an object (category, name, image, description, price, created, user_id)
    """
    this method selects the listing with the requested id and returns information from the database, in a format that can easily be render to html
    with this method, all listing have to be retrieved manually by providing the id in the address bar, e.g. marketplace.flask/1 for the first listing
    further implementation should show all listings with basic information like main picture, price and name
    listings are clickable and return the id to the db, requesting additional information and displaying the full listing
    """
    try:
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            # After research the method was updated to include a parameterized, preventing possibly unwanted user input that can alter the database (SQL-injection)
            cur.execute("SELECT id, category, name, image, description, price, created, user_id FROM Listings WHERE id=?", (id,))
            row = cur.fetchone()
            if row:
                # this method of extracting the data from sql uses a static approach
                listing = {
                    'id': row[0],
                    'category': row[1],
                    'name': row[2],
                    'image': row[3],
                    'description': row[4],
                    'price': row[5],
                    'created': row[6],
                    'user_id': row[7]
                }
                cur.execute("SELECT name FROM User WHERE id=?", (listing['user_id'],))
                row = cur.fetchone()
                print(row)
                listing['user_name'] = row[0]
            else:
                listing = None
    except sqlite3.Error as e:
        # this prints the sqlite3 Error to console if some error occurs
        print(f"Database error: %s" %e)
        listing = None
    return listing



def get_all_listings(*args):
    try:
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            # After research the method was updated to include a parameterized, preventing possibly unwanted user input that can alter the database (SQL-injection)
            if 'user_id' in args:
                cur.execute("SELECT id, category, name, image, price, description, created, user_id FROM Listings WHERE user_id=(?)", (args[1],))
            else:
                cur.execute("SELECT id, category, name, image, price, description, created, user_id FROM Listings")
            rows = cur.fetchall()
            listings = []
            index = 0
            for listing in rows:
                listings.append({"id": listing[0], 
                            "category": listing[1], 
                            "name": listing[2], 
                            "image": listing[3], 
                            "description": listing[5], 
                            "price": listing[4], 
                            "created": listing[6], 
                            "user_name": listing[7]
                            })
                index += 1
            return listings
    except sqlite3.Error as e:
        # this prints the sqlite3 Error to console if some error occurs
        print(f"Database error: %s" %e)
        return rows


def delete_listings(*args):
    try:
        # Connect to the SQLite database
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE from Listings WHERE id=(?)", (args[0],))
            connection.commit()
            if True in args:
                cursor.execute(f"SELECT id, name from Listings WHERE id={args[0]}")
                rows = cursor.fetchone()
                # Check if any rows were fetched
                if rows:
                    print(f"could not delete listing with id {args[0]}, no error")
                else:
                    print(f"deleted listing with id {args[0]} successful")
    except sqlite3.Error as e:
        # Print the error if one occurs
        print(f"Database error: {e}")



"""
def get_listings_user(user_id):
    try:
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            # After research the method was updated to include a parameterized, preventing possibly unwanted user input that can alter the database (SQL-injection)
            cur.execute("SELECT id, name, image, price, created FROM Listings WHERE user_id='?'", (user_id, ))
            rows = cur.fetchall()
            listings = []
            index = 0
            print(rows)
            for listing in rows:
                listings.append({"id": listing[0], 
                            "category": listing[1], 
                            "name": listing[2], 
                            "image": listing[3], 
                            "description": listing[5], 
                            "price": listing[4], 
                            "created": listing[6], 
                            "user_name": listing[7]
                            })
                index += 1
            print(listings)
            return listings
    except sqlite3.Error as e:
        # this prints the sqlite3 Error to console if some error occurs
        print(f"Database error: %s" %e)
        listings = False
        return listings
    
"""
"""
def new_listing(listing):
    # this method uses a direct approach to redirect the form data to sql
    # the keywords of the html form are named to match the sql columns to achieve this
    # this approach is intended to make the application scalable if additional information will be implemented for the Listings table
    # the alternative would be to extract the data of the form using multiple variables and insert them seperately
    # image and user_id will be implemented later 
    # image upload method saves the image to resources and creates a reference
    # user_id will be handled by login
    try:
        # Extract the keys (column names) and values from the dictionary
        # this method of injecting the data to sql uses a dynamic approach
        del listing['post']
        columns = ', '.join(listing.keys())
        placeholders = ', '.join(['?'] * len(listing))
        values = tuple(listing.values())
        # Construct the SQL query
        sql = f"INSERT INTO Listings ({columns}) VALUES ({placeholders})"
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            cur.execute(sql, values)
            connection.commit()
            connection.close()
            return True
    except sqlite3.Error as e:
        # Print the sqlite3 Error to console if some error occurs
        print(f"Database error: {e}")
        return False

"""
