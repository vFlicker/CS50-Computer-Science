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
        name TEXT NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price REAL NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

SELECT
    t.symbol,
    SUM(t.shares) AS shares_count,
    t.price,
    SUM(t.price) AS total
FROM transactions AS t
    JOIN users AS u ON t.user_id = u.id
WHERE t.user_id = 2
GROUP BY symbol
HAVING COUNT(symbol);

SELECT
    SUM(t.price) AS total,
    u.cash
FROM transactions AS t
    JOIN users AS u ON t.user_id = u.id
WHERE t.user_id = 2;

CREATE TABLE sqlite_sequence( name, seq );

CREATE UNIQUE INDEX username ON users (username);