import sqlite3


def print_all_listings():
    try:
        # Connect to the SQLite database
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            
            # Execute the query to fetch all users
            cursor.execute("SELECT id, name, price, user_id, image FROM Listings")
            rows = cursor.fetchall()
            
            # Check if any rows were fetched
            if rows:
                print(f"{'listing_id':<5} {'name':<20} {'price':<10} {'user':<5} {'image':<20}")
                print("="*50)
                for row in rows:
                    id = row[0] if row[0] is not None else 'N/A'
                    name = row[1] if row[1] is not None else 'N/A'
                    price = row[2] if row[2] is not None else 'N/A'
                    user = row[3] if row[3] is not None else 'N/A'
                    image = row[4] if row[4] is not None else 'N/A'
                    print(f"{id:<5} {name:<20} {price:<10} {user:<5} {image:<20} ")
            else:
                print("No Listings found.")
    
    except sqlite3.Error as e:
        # Print the error if one occurs
        print(f"Database error: {e}")
    


def print_all_users():
    try:
        # Connect to the SQLite database
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            
            # Execute the query to fetch all users
            cursor.execute("SELECT id, name, password_hash FROM User")
            user_rows = cursor.fetchall()
            
            # Check if any rows were fetched
            if user_rows:
                print(f"{'ID':<10} {'Username':<10} {'Password Hash'}")
                print("="*50)
                for row in user_rows:
                    user_id = row[0] if row[0] is not None else 'N/A'
                    username = row[1] if row[1] is not None else 'N/A'
                    password_hash = row[2] if row[2] is not None else 'N/A'
                    print(f"{user_id:<10} {username:<10} {password_hash}")
            else:
                print("No users found.")

    except sqlite3.Error as e:
        # Print the error if one occurs
        print(f"Database error: {e}")


    
def create_listings_dummy(arg):
    for id in range(arg):
        try:
            # Connect to the SQLite database
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                
                # Execute the query to fetch all users
                name = "Dummy"
                description = "I am a dummy"
                cursor.execute(f"INSERT INTO Listings (name, description, price, category, user_id) VALUES (?,?,?,?,?)", (name,description,100,1,1))
                connection.commit()
        except sqlite3.Error as e:
            # Print the error if one occurs
            print(f"Database error: {e}")



# Run the function to print all users
if __name__ == "__main__":
#    create_listings_dummy()
    delete_listings(14, 15, 16)
    print_all_users()
    print_all_listings()