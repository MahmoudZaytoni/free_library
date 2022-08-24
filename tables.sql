-- CREATE TABLE IF NOT EXISTS Customers (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     firstname,
--     lastname);


CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cover varchar(255) NOT NULL,
    title varchar(255) NOT NULL,
    author varchar(255) NOT NULL,
    description_book TEXT
);