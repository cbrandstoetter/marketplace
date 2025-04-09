<h3>Educational project to learn web development in Python Flask. A fully functional second hand market where you can register as a user, post the items you want to sell, look at items of other people and message each other.

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
  <li><strong>Deployment:</strong> Gunicorn will be used as an interface, when the app gets deployed to a production environment. The Sqlite database is initialized manually</li>
</ul>