DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_number INTEGER NOT NULL,
    UNIQUE(name, phone_number)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    racket_id INTEGER NOT NULL,
    date DATE NOT NULL,
    mains_tension INTEGER NOT NULL,
    crosses_tension INTEGER NOT NULL DEFAULT(mains_tension),
    mains_string_id INTEGER NOT NULL FOREIGN KEY,
    crosses_string_id INTEGER DEFAULT(mains_string_id),
    CONSTRAINT customer_id FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id),
    CONSTRAINT racket_id FOREIGN KEY (racket_id)
    REFERENCES rackets(racket_id),
    CONSTRAINT mains_string_id FOREIGN KEY (string_id)
    REFERENCES strings(string_id),
    CONSTRAINT crosses_string_id FOREIGN KEY (string_id)
    REFERENCES strings(string_id)
);

CREATE TABLE rackets (
    racket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER CHECK(year >= 1900),
    head_size INTEGER NOT NULL CHECK(head_size > 0),
    grip_size FLOAT NOT NULL CHECK(grip_size > 4.0),
    weight INTEGER NOT NULL CHECK(weight > 0),
    stringing_pattern TEXT NOT NULL,
    swing_weight FLOAT (swing_weight >= 0),
    balance FLOAT (balance >= 0),
    stiffness INTEGER CHECK(stiffness >= 0)
);

CREATE TABLE strings (
    string_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    gauge INTEGER NOT NULL CHECK(gauge > 0),
    shape TEXT,
    type TEXT NOT NULL
);

-- CREATE INDEX idx_songs_artist_title ON songs(artist, title);
-- CREATE INDEX idx_songs_year ON songs(year);
-- CREATE INDEX idx_songs_play_count ON songs(play_count);

