import os
import sqlite3
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# flask --app app run
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

limiter = Limiter(key_func=get_remote_address, default_limits=["100 per hour"])
limiter.init_app(app)

app.config['DEBUG'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['UPLOAD_FOLDER'] = 'static'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.getcwd(), 'robots.txt')


@app.route('/test')
@limiter.limit("5 per minute")  # Additional limit for this route
def test_route():
    return jsonify(message="This route is rate-limited.")


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded. Try again later."), 429

# def getCategoryFromId(categoryId):
#     categories = [
#         "Toys",e
#         "Electronics",
#         "Clothing",
#         "Books",
#         "Furniture",
#         "Tools",
#         "Sports",
#         "Games",
#         "Music",
#         "Antiques",
#         "Vehicles",
#         "Real Estate",
#         "Garden",
#         "Computers",
#         "Accessories"
#     ]
#     try:
#         return categories[categoryId - 1]  # subtract 1 because lists are 0-indexed
#     except IndexError:
#         return "Unknown"


class User(UserMixin):
    def __init__(self, id, username, password_hash, profile_image):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.profile_image = profile_image

    @staticmethod
    def get(user_id):
        # returns id, username, password hash
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password_hash, profile_image FROM User WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            return None
        return User(user[0], user[1], user[2], user[3])

    @staticmethod
    def check_messages():
        try:
            # Connect to the SQLite database
            with sqlite3.connect('database.db') as connection:
                cur = connection.cursor()
                rows = cur.execute('select read from Messages where user_receive=?',(current_user.id,)).fetchall()
                if any(row[0]==0 for row in rows):
                    return True
        except sqlite3.Error as e:
            # Flash the error if one occurs
            flash('database error')

    @staticmethod
    def find_by_username(username):
        # finds user by username
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password_hash, profile_image FROM User WHERE name = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            return None
        return User(user[0], user[1], user[2], user[3])

    def verify_password(self, password):
        # processes User{password: "xyz"} and entered password second argument
        return check_password_hash(self.password_hash, password)

class Message:
    def __init__(self, message, created, user_send, user_receive, 
                 user_send_username, user_receive_username, listing_id):
        self.message = message
        self.created = created
        self.user_send = user_send
        self.user_receive = user_receive
        self.user_send_username = user_send_username
        self.user_receive_username = user_receive_username
        self.listing_id = listing_id


def listing_by_id(id):
    """
    this method selects the listing with the requested id from the database;
    keys -> id, category, name, image, description, price, created, user_id
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
                listing['user_name'] = row[0]
            else:
                listing = None
    except sqlite3.Error as e:
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
            return listings[1:]
    except sqlite3.Error as e:
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
    except sqlite3.Error as e:
        # Flash the error if one occurs
        flash("Database error occurred.")
        # WIP add error logging


# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # calls get() function in User methods
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to login or create an account first")
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO User (name, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            conn.close()
            flash('you registered successfully!')
            return redirect(url_for('register'))
        except sqlite3.Error as e:
            if str(e) == "UNIQUE constraint failed: User.name":
                flash('username already taken.')
            else:
                flash('unknown database error')
    
    return render_template('register.html')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    try:
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            if(User.find_by_username('Demo_user')):
                cur.execute('delete from User where name=?', ('Demo_user',))
            cur.execute('insert into User (name, password_hash) VALUES (?, ?)', (
                'Demo_user',
                'scrypt:32768:8:1$rS1v7gcBStl4KTn2$bf21b154714df13126bdd814eceaf5eb4adf380e9b730dbe4c2662b90147aa3607ee9107e4060ecdf07a4a388235a3668e115282d167cb96fb91cf1a48bc73fb'
            ))
            connection.commit()
            user = User.find_by_username('Demo_user')
            login_user(user)
            cur.execute('insert into Messages (subject, message, user_send, user_receive, listing_id) ' \
                        'values (?, ?, ?, ?, ?)', (
                            'Welcome',
                            'Here you can find your messages. You can message a listing to test it out.',
                            1,
                            user.id,
                            1
                        ))
    except sqlite3.Error as e:
        flash('database error')
    flash("Welcome, to the homepage! You are logged in as a Demo-User.")
    return redirect(url_for('marketplace'))
    


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="Too many login attempts. Please try again later.")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('marketplace'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Clear any remaining flash messages
    session.pop('_flashes', None)
    return redirect(url_for('marketplace'))

def allowed_file(filename):
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    if not('.' in filename.filename and filename.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        filename.seek(0)
        return False
    if len(filename.read()) > MAX_FILE_SIZE:
        filename.seek(0)
        return False
    return True


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file):
            filename = f"{current_user.id}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE User SET profile_image = ? WHERE id = ?", (filename, current_user.id))
            conn.commit()
            conn.close()
            return redirect(url_for('profile'))
        else:
            flash("Only .jpeg and .png allowed. Maximum file size: 5MB")
            return redirect(url_for('profile'))


    return render_template('profile.html', user=current_user)


@app.route("/yourlistings", methods=['POST', 'GET'])
@login_required
def profile_listings():
    listings = get_all_listings('user_id', current_user.id)
    if not listings:
        flash('You have no listings yet. please create a listings to show and edit listings')
        return redirect(url_for('profile'))
    if request.method == 'POST':
        form = request.form
        # edit the listing and return to listing page
        if 'edit' in form:
            flash('You have no listings yet. please create a listings to show and edit listings')

            """
            edit button added in future update!
            """
        # delete the listing and return to listing page
        elif 'delete' in form:
            # get id from form and delete.
            id = request.form['delete']
            delete_listings(id, True)
        return redirect(url_for('profile_listings'))


    return render_template('profile-listings.html', listings=listings, user=current_user)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def marketplace():
    return render_template('new-design.html')


@app.route("/listing/<id>")
def get_listing(id):
    try:
        # this returns listing data as values for html
        # listing will be given as a dictionary that can be accessed with jinja at the desired place for flexible design
        # escape is used for better security, preventing harmful user input
        listing = listing_by_id(int(id))
        if not listing:
            abort(404)
        return render_template('listing.html', listing = listing)
    except sqlite3.Error as e:
        # return 404 if an error occurs
        abort(404)


@app.route("/newlisting", methods=["POST", "GET"])
# this method sends form data to be processed by db handler
# the keywords of the html form are named to match the sql columns
def post_listing():
    if current_user.is_authenticated:
        if request.method == 'POST':
            lst = request.form.to_dict()
            # placeholder for future implementations: user_id, category, image 
            lst["user_id"] = current_user.id
            # get and save file
            file = request.files.get('image')
            if file:
                if allowed_file(file):
                    filename = f"{current_user.id}_lst_{file.filename}"
                    lst["image"] = filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash("Only .jpeg and .png allowed. Maximum file size: 5MB")
                    return render_template('listing-creation.html', user=current_user)
            else:
                lst["image"] = 'default_listings_image.png'
            # save listing to database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Listings (name, description, price, category, user_id, image) VALUES (?, ?, ?, ?, ?, ?)", 
                           (lst["name"], lst["description"], lst["price"], lst["category"], lst["user_id"], lst["image"]))
            conn.commit()
            conn.close()
            flash("listing was posted!")
            return redirect(url_for('marketplace'))
    # handle if user is not logged in
    else:
        return redirect(url_for('register'))

    return render_template('listing-creation.html', user=current_user)


@app.route("/listings")
# this route shows all listings with image, name, price
def show_listings():
    listings = get_all_listings()
    if not listings:
        flash("No listings available at the moment.", "warning")  # Flash a message
        return redirect(url_for('marketplace'))  # Redirect to the same route to re-render the page
    return render_template('listings.html', listings = listings)


@app.route("/messaging/<id>", methods=["POST", "GET"])
@login_required
def send_message(id):
    listing = listing_by_id(id)
    if not listing:
        abort(404)
    if request.method == 'POST':
        message = request.form['message']
        try:
            # Connect to the SQLite database
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                subject = ''
                cursor.execute(f"INSERT INTO Messages (subject, message, user_send, user_receive, listing_id) VALUES (?,?,?,?,?)", (subject, message, current_user.id, listing['user_id'], listing['id']))
                connection.commit()
                flash('message sent')
        except sqlite3.Error as e:
            # Flash the error if one occurs
            flash('database error')
    return render_template('send-message.html', listing = listing)


@app.route("/profile/<id>", methods=["POST", "GET"])
def get_profile(id):
    return "profile will be shown here"


@app.route("/messages")
@login_required
def get_messages():
    try:
        # Connect to the SQLite database
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM Messages where user_receive=? OR user_send=? order by created DESC", (current_user.id, current_user.id))
            messages = []
            for lst in cur.fetchall():
                messages.append({'id':lst[0],'message':lst[2],'created':lst[3],'listing_id':lst[6]})
            listing_ids = [listing['listing_id'] for listing in messages]
            listing_ids = list(dict.fromkeys(listing_ids))
            listings_overview = []
            for listing_id in listing_ids:
                cur.execute("select name, price, image from listings where id=?",(listing_id,))
                data = cur.fetchone()
                # overview data to dict
                last_message = cur.execute("select message,read,user_receive,user_send from Messages where (user_receive=? OR user_send=?) AND listing_id=? order by created DESC",(current_user.id,current_user.id,listing_id)).fetchone()
                # check if a new message in chat for later implementation:
                contact = last_message[2] if not last_message[2] == current_user.id else last_message[3]
                contact_name = User.get(contact).username
                is_new = (True if (last_message[1]==0 and last_message[2]==current_user.id) else False)
                listings_overview.append({'name':data[0],'price':data[1],'image':data[2],'id':listing_id,'new_message':is_new,'last':last_message[0], 'contact':contact_name})
    except sqlite3.Error as e:
            # Flash the error if one occurs
            flash('database error')
    
    return render_template('messages.html', listings=listings_overview)

@app.route("/messages/<id>", methods=["GET", "POST"])
@login_required
def message_get(id):
    if request.method == 'POST':
        try:
            # Connect to the SQLite database
            with sqlite3.connect('database.db') as connection:
                cur = connection.cursor()
                # get message form
                message = request.form['message']
                receiver = request.form['receiver']
                cur.execute('insert into Messages (message,user_send,user_receive,listing_id) values (?,?,?,?)',(message,current_user.id,receiver,id))
                connection.commit()
        except sqlite3.Error as e:
                # Flash the error if one occurs
                flash('database error')
        
    try:
        # Connect to the SQLite database
        with sqlite3.connect('database.db') as connection:
            cur = connection.cursor()
            # delete the unread parameter if chat is opened
            cur.execute("UPDATE Messages SET read=1 where (user_receive=?) AND listing_id=?", (current_user.id,id))
            connection.commit()
            cur.execute("SELECT message,created,user_send FROM Messages where (user_receive=? OR user_send=?) AND listing_id=? order by created ASC", (current_user.id,current_user.id,id))
            messages = []
            for lst in cur.fetchall():
                messages.append({'message':lst[0],'created':lst[1],'user':(True if lst[2]==current_user.id else False)})
            user_with = cur.execute("SELECT user_send, user_receive FROM Messages where (user_receive=? OR user_send=?) AND listing_id=?", (current_user.id,current_user.id,id)).fetchone()
            user_with = [id for id in user_with if id!=current_user.id]
    except sqlite3.Error as e:
            # Flash the error if one occurs
            flash('database error')
    
    return render_template('messages-chat.html', messages=messages, user_with=user_with)