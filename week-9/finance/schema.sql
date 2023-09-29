CREATE TABLE
  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
  );

CREATE TABLE
  transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    quote_name TEXT NOT NULL,
    quote_symbol TEXT NOT NULL,
    quote_shares INTEGER NOT NULL,
    quote_price REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
  );

CREATE TABLE
  sqlite_sequence (name, seq);

CREATE UNIQUE INDEX username ON users (username);