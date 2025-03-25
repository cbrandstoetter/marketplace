<h3>Educational project to learn web development in Python Flask. A fully functional second hand market where you can register as a user, post the items you want to sell, look at items of other people and message each others.
I deployed the Application on the provider "digital ocean" once for practice. I used Gunicorn to serve the application on the cloud.</h3>

<h2>Features:</h2>
<ul>
  <li>Register as a user and upload a profile picture</li>
  <li>Create listings for items</li>
  <li>Upload pictures of the items</li>
  <li>Advertise your listing with text and images</li>
  <li>Browse and search for current listings</li>
  <li>Message the user if you want to buy from them</li>
  <li>View your messages and communicate back and forth</li>
  <li>Other users are notified with an indicator on their landing page</li>
  <li>Edit and delete your listings</li>
</ul>

<h2>Technologies and their Implementation:</h2>
<ul>
  <li><strong>Framework:</strong> Python Flask is used as a framework for its ease of use and simple syntax</li>
  <li><strong>User Handling:</strong> Flask-login is used to manage user sessions</li>
  <li><strong>Password Hashing:</strong> Passwords are hashed with Werkzeug.security. No plain-text passwords are saved in the database</li>
  <li><strong>Key Handling:</strong> The secret key for Flask sessions is retrieved from an environment variable, ensuring that no keys are exposed in the source code</li>
  <li><strong>Rendering:</strong> Pages are generated dynamically using Jinja templates, which allow for control structures (such as loops) to generate HTML</li>
  <li><strong>Database:</strong> SQLite3 is used with manual queries to practice SQL syntax. With my current knowledge, I would transition to using an ORM, such as SQLAlchemy, for future projects</li>
</ul>

<h2>Landing page with simple UI, basic CSS</h2>
<img src="static/docs/screenshot/landing_page.png" width="600px" alt="UI screenshot">

<h2>Shows an error, only logged in users can post something</h2>
<img src="static/docs/screenshot/error.png" width="600px" alt="Error Handling">

<h2>Register page</h2>
<img src="static/docs/screenshot/register.png" width="600px" alt="Register">

<h2>Login page</h2>
<img src="static/docs/screenshot/login.png" width="600px" alt="Login">

<h2>Landing page now shows messages and profile, user can logout</h2>
<img src="static/docs/screenshot/profile.png" width="600px" alt="Landing Page logged in">

<h2>Post an item, providing information. You can upload a picture that gets stored in the database</h2>
<img src="static/docs/screenshot/item_description.png" width="600px" alt="Create listing">

<h2>Show all listings that are posted, click on the listings you are interested in</h2>
<img src="static/docs/screenshot/listings.png" width="600px" alt="Show all listings">

<h2>Shows the item in a new page, with all information. Placeholder for categories, work in progress</h2>
<img src="static/docs/screenshot/item_page.png" width="600px" alt="Listing page">

<h2>I can send a message to the user that posted the item</h2>
<img src="static/docs/screenshot/send_message.png" width="600px" alt="Message window">

<h2>I can see the messages I sent and received</h2>
<img src="static/docs/screenshot/messages_page.png" width="600px" alt="Message page">

<h2>A minimal chat window, has to be reloaded due to server-side rendering</h2>
<img src="static/docs/screenshot/minimal_chat.png" width="600px" alt="Chat">

<h2>The other user got notified that they have a new message with the red color on messages</h2>
<img src="static/docs/screenshot/message_notification.png" width="600px" alt="Message notification">

<h2>I can see the new message in my messages. Messages I haven't read yet have this red indicator</h2>
<img src="static/docs/screenshot/new_message.png" width="600px" alt="New message indicator">

<h2>I can look at my profile and show my listings. Here I can edit and delete them</h2>
<img src="static/docs/screenshot/my_listings.png" width="600px" alt="Edit and delete listings">
