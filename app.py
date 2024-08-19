import os
import sqlite3
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from db import listing_by_id, new_listing, get_all_listings, delete_listings

# flask --app app run
app = Flask(__name__)
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)


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
    def find_by_username(username):
        # finds user by username
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password_hash, profile_image FROM User WHERE name = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            print("username is not in database")
            return None
        return User(user[0], user[1], user[2], user[3])

    def verify_password(self, password):
        # processes User{password: "xyz"} and entered password second argument
        return check_password_hash(self.password_hash, password)


# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # calls get() function in User methods
    return User.get(user_id)


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
            print('New user registered!')
            flash('you registered successfully!')
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            print(f"database error: {e}")
            print(e)
            if str(e) == "UNIQUE constraint failed: User.name":
                flash('username already taken.')
            else:
                flash('unknown database error')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        user = User.find_by_username(username)
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Clear any remaining flash messages
    session.pop('_flashes', None)
    return redirect(url_for('index'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = f"{current_user.id}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE User SET profile_image = ? WHERE id = ?", (filename, current_user.id))
            conn.commit()
            conn.close()
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
        print(form)
        # edit the listing and return to listing page
        if 'edit' in form:
            print('edit\n#############')
            print(request.form['edit'])
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
def index():
    if current_user.is_authenticated:
        print(f"User {current_user.username} is logged in")
    else:
        print("No user is logged in")
    return render_template('index.html')


@app.route("/<id>")
def get_listing(id):
    try:
        # this returns listing data as values for html
        # listing will be given as a dictionary that can be accessed with jinja at the desired place for flexible design
        # see listing_by_id in db.py for backend implementation
        # escape is used for better security, preventing harmful user input
        listing = listing_by_id(int(id))
        print(listing['user_name'])
        return render_template('listing.html', listing = listing)
    except sqlite3.Error as e:
        print(f"error: {e}")
        # return 404 if an error occurs
        abort(404)


@app.route("/newlisting", methods=["POST", "GET"])
# this method sends form data to be processed by db handler
# the keywords of the html form are named to match the sql columns to achieve this
def post_listing():
    if current_user.is_authenticated:
        if request.method == 'POST':
            lst = request.form.to_dict()
            # placeholder for future implementations: user_id, category, image 
            lst["category"] = 1
            lst["user_id"] = current_user.id
            # get and save file
            file = request.files.get('image')
            if file and allowed_file(file.filename):
                filename = f"{current_user.id}_lst_{file.filename}"
                lst["image"] = filename
                for item in lst:
                    print(item)
                    print(lst[item])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
            return redirect(url_for('index'))
    # handle if user is not logged in
    else:
        flash("you have to be create an account to create a listing.")
        return render_template('index.html')

    return render_template('listing-creation.html', user=current_user)


@app.route("/listings")
# this route shows all listings with image, name, price
def show_listings():
    listings = get_all_listings()
    if not listings:
        return render_template('error.html', errormessage = "The Listings could not be displayed, and unknown error occurred")
    return render_template('listings.html', listings = listings)

