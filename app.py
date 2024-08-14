from flask import Flask, render_template, request, flash
from markupsafe import escape
from werkzeug.exceptions import abort
from db import listing_by_id
from db import new_listing
from db import get_all_listings
from flask_login import LoginManager

app = Flask(__name__)
# flask --app app run
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def index():
    return render_template('index.html')



@app.route("/<id>")
def get_listing(id):
    try:
        # this returns listing data as values for html
        # listing will be given as a dictionary that can be accessed with jinja at the desired place for flexible design
        # see listing_by_id in db.py for backend implementation
        # escape is used for better security, preventing harmful user input
        listing_id = escape(listing_by_id(int(id)))
        return render_template('listing.html', listing = listing_by_id(listing_id))
    except:
        # return 404 if an error occurs
        abort(404)


@app.route("/newlisting")
def create_listing():
    return render_template('listing-creation.html')


@app.route("/newlisting", methods=["POST"])
# this method sends form data to be processed by db handler
# the keywords of the html form are named to match the sql columns to achieve this
def post_listing():
    listing_data = request.form.to_dict()

    # placeholder for future implementations: user_id, category, image 
    listing_data["user_id"] = "Not implemented yet"
    listing_data["category"] ="Not implemented yet"
    listing_data["image"] = "Not implemented yet"
    # check if listing_data can process the data
    if new_listing(listing_data):
        flash("successfully submitted")
        return index()
    else:
        return render_template('error.html', errormessage = "The Listing could not be processed, check the entried data again")

@app.route("/listings")
# this route shows all listings with image, name, price
def show_listings():
    listings_data = get_all_listings()
    if not listings_data:
        return render_template('error.html', errormessage = "The Listings could not be displayed, and unknown error occurred")
    else: 
        return render_template('listings.html', listings = listings_data)
