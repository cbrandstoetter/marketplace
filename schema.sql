DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Listings;
DROP TABLE IF EXISTS Messages;

CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL, 
    profile_image TEXT
);

CREATE TABLE Listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category INTEGER NOT NULL,
    name TEXT NOT NULL,
    image TEXT,
    description TEXT NOT NULL,
    price REAL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);


CREATE TABLE Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    message TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_send INTEGER NOT NULL,
    user_receive INTEGER NOT NULL,
    listing_id INTEGER NOT NULL,
    read INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(user_send) REFERENCES User(id),
    FOREIGN KEY(user_receive) REFERENCES User(id), 
    FOREIGN KEY(listing_id) REFERENCES Listings(id)
);