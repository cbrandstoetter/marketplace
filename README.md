Educational project to learn web development in Python Flask. A fully functional second hand market where you can register as a user, post the items you want to sell, look at items of other people and message each others.
I deployed the Application on the provider "digital ocean" once for practice. I used Gunicorn to serve the application on the cloud.

Features:
- register as a user, upload a profile picture
- create listings
- upload pictures of the item
- advertise your listing with text and pictures
- look for current listings
- message the user if you want to buy from them
- look at your messages and write back and forth
- other user gets notified on his landing page with an indicator
- edit and delete your listings

Technologies and their implementation:
- Python Flask is used as a framework, for its ease of use and simple syntax
- Flask-login is used to implement user handling
- password hashing, passwords are stored in the database as a hash
- the secret key for hashing is stored in the environment to protect the key
- pages are generated dynamically, using jinja template
- jinja template allows control structures, this is utilized for html generation (for loop)
- sqlite3 as database with manual queries to practice SQL syntax. With my current knowledge i would transition to using an ORM, SQLAlchemy in the case of flask

<h2>Landing page with simple UI, basic CSS</h2>
<img src="static/docs/screenshot/landing_page.png" width="600px" alt="UI screenshot">

<h2>Shows an error, only logged in users can post something</h2>
<img src="static/docs/screenshot/error.png" alt="Error Handling">

<h2>Register page</h2>
<img src="static/docs/screenshot/register.png" alt="Register">

<h2>Login page</h2>
<img src="static/docs/screenshot/login.png" alt="Login">

<h2>Landing page now shows messages and profile, user can logout</h2>
<img src="static/docs/screenshot/profile.png" alt="Landing Page logged in">

<h2>Post an item, providing information. You can upload a picture that gets stored in the database</h2>
<img src="static/docs/screenshot/item_description.png" alt="Create listing">

<h2>Show all listings that are posted, click on the listings you are interested in</h2>
<img src="static/docs/screenshot/listings.png" alt="Show all listings">

<h2>Shows the item in a new page, with all information. Placeholder for categories, work in progress</h2>
<img src="static/docs/screenshot/item_page.png" alt="Listing page">

<h2>I can send a message to the user that posted the item</h2>
<img src="static/docs/screenshot/send_message.png" alt="Message window">

<h2>I can see the messages I sent and received</h2>
<img src="static/docs/screenshot/messages_page.png" alt="Message page">

<h2>A minimal chat window, has to be reloaded due to server-side rendering</h2>
<img src="static/docs/screenshot/minimal_chat.png" alt="Chat">

<h2>The other user got notified that they have a new message with the red color on messages</h2>
<img src="static/docs/screenshot/message_notification.png" alt="Message notification">

<h2>I can see the new message in my messages. Messages I haven't read yet have this red indicator</h2>
<img src="static/docs/screenshot/new_message.png" alt="New message indicator">

<h2>I can look at my profile and show my listings. Here I can edit and delete them</h2>
<img src="static/docs/screenshot/my_listings.png" alt="Edit and delete listings">
