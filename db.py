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
            cur.execute("SELECT category, name, image, description, created, user_id FROM Listings WHERE id=?", (id,))
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
            else:
                listing = None
    except sqlite3.Error as e:
        # this prints the sqlite3 Error to console if some error occurs
        print(f"Database error: %s" %e)
        listing = None
    return listing


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
            return True
    except sqlite3.Error as e:
        # Print the sqlite3 Error to console if some error occurs
        print(f"Database error: {e}")
        return False


def get_all_listings():
    try:
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            # After research the method was updated to include a parameterized, preventing possibly unwanted user input that can alter the database (SQL-injection)
            cur.execute("SELECT id, category, name, image, price, description, created, user_id FROM Listings")
            rows = cur.fetchall()
            if rows:
                return rows
            else:
                rows = None
    except sqlite3.Error as e:
        # this prints the sqlite3 Error to console if some error occurs
        print(f"Database error: %s" %e)
        rows = False
    return rows