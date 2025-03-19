Flask project, a second hand market.

Features:
- register as a user, upload a profile picture
- create listings
- advertise your listing with text and pictures
- look for current listings
- message the user if you want to buy from them
- look at your messages and write back
- edit and delete your listings

Technology:
- Python with Flask framework
- static html with jinja template
- sqlite3 as database with manual queries
- User handling with flask-login
- Password encryption

Landing page
![Landing page](static/docs/screenshot/landing-page.png)

Shows an error, only logged in users can post something
![Error Handling](static/docs/screenshot/error.png)

Register page
![Register](static/docs/screenshot/register.png)

Login page
![Register](static/docs/screenshot/login.png)

Landing page now shows messages and profile, user can logout
![Register](static/docs/screenshot/profile.png)

Post an item, providing information. You can upload a picture that gets stored in the database
![Register](static/docs/screenshot/item_description.png)

Show all listings that are posted, click on the listings you are interested in
![Register](static/docs/screenshot/listings.png)

Shows the item in a new page, with all information. Placeholder for categories, work in progress
![Register](static/docs/screenshot/item_page.png)

I can send a message to the user that posted the item
![Register](static/docs/screenshot/send_message.png)

I can see the messages i sent and received
![Register](static/docs/screenshot/messages_page.png)

A minimal chat window, has to be reloaded due to server side rendering
![Register](static/docs/screenshot/minimal_chat.png)

The other user got notified that he has a new message with the red color on messages
![Register](static/docs/screenshot/message_notification.png)

I can see the new message in my messages. Messages i haven't read yet have this red indicator
![Register](static/docs/screenshot/new_message.png)
