from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get data
    user_id = session["user_id"]

    # Query database for user cash
    user_cash = db.execute(
        """
        SELECT
            cash
        FROM
            users
        WHERE id = ?
        """,
        user_id,
    )[0]["cash"]

    # Query database for user stocks
    stocks = db.execute(
        """
        SELECT
            quote_name AS name,
            quote_symbol AS symbol,
            SUM(quote_shares) AS shares
        FROM
            transactions
        WHERE
            user_id = ?
        GROUP BY
            quote_symbol HAVING shares > 0
        """,
        user_id,
    )

    # Add actual price to user's stocks
    for i, stock in enumerate(stocks):
        quote = lookup(stock["symbol"])
        stocks[i]["price"] = quote["price"]

    # Calculate total
    total = user_cash + sum(stock["price"] * stock["shares"] for stock in stocks)

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("index.html", stocks=stocks, cash=user_cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get from data
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure the symbol was submitted
        if not symbol:
            return apology("missing symbol", 400)

        # Look up quote for symbol
        quote = lookup(symbol)

        # Ensure the symbol is correct
        if quote is None:
            return apology("invalid symbol", 400)

        # Ensure the shares is correct
        try:
            shares = int(shares)

            if shares < 1:
                raise ValueError()
        except ValueError:
            return apology("invalid shares", 400)

        # Get user id and price
        user_id = session["user_id"]
        price_per_share = quote["price"]

        # Query database for user cash
        user_cash = db.execute(
            """
            SELECT
                cash
            FROM
                users
            WHERE id = ?
            """,
            user_id,
        )[0]["cash"]

        # Calculate updated cash
        updated_cash = user_cash - price_per_share * shares

        if updated_cash < 0:
            return apology("can't afford")

        # Start transaction
        db.execute("BEGIN TRANSACTION")

        # Withdraw money from the user's account
        db.execute(
            """
            UPDATE users
            SET
                cash = :cash
            WHERE
                id = :id
            """,
            id=user_id,
            cash=updated_cash,
        )

        # Add a new transaction to the list of transactions
        db.execute(
            """
            INSERT INTO
                transactions (
                    user_id,
                    quote_symbol,
                    quote_name,
                    quote_shares,
                    quote_price
                )
            VALUES
                (
                    :user_id,
                    :quote_symbol,
                    :quote_name,
                    :quote_shares,
                    :quote_price
                )
            """,
            user_id=user_id,
            quote_symbol=quote["symbol"],
            quote_name=quote["name"],
            quote_shares=shares,
            quote_price=price_per_share,
        )

        # End transaction
        db.execute("COMMIT")

        # Show success message
        flash("Bought!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute(
        """
        SELECT
            quote_symbol AS symbol,
            quote_shares AS shares,
            quote_price AS price,
            created_at AS transacted
        FROM
            transactions
        WHERE user_id = ?
        """,
        session["user_id"],
    )

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Get from data
    username = request.form.get("username")
    password = request.form.get("password")

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        user = db.execute(
            """
            SELECT
                *
            FROM
                users
            WHERE
                username = ?
            """,
            username,
        )

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get form data
        symbol = request.form.get("symbol")

        # Ensure the symbol was submitted
        if not symbol:
            return apology("missing symbol", 400)

        # Look up quote for symbol
        quote = lookup(symbol)

        # Ensure the symbol is correct
        if quote is None:
            return apology("invalid symbol", 400)

        # Redirect user to quoted page
        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:  # Ensure the username was submitted
            return apology("must provide username", 400)
        elif not password:  # Ensure the password was submitted
            return apology("must provide password", 400)
        elif password != confirmation:  # Ensure passwords were matched
            return apology("the passwords do not match", 400)

        # Query database for username
        user = db.execute(
            """
            SELECT
                *
            FROM
                users
            WHERE
                username = ?
            """,
            username,
        )

        # Ensure username does not exists
        if len(user) == 1:
            return apology("the username already exists", 400)

        # Generate password hash
        hashed_password = generate_password_hash(password)

        # Add the user to the database
        db.execute(
            """
            INSERT INTO
                users (
                    username,
                    hash
                )
            VALUES
                (
                    :username,
                    :hash
                )
            """,
            username=username,
            hash=hashed_password,
        )

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get current user id
    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get from data
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure the symbol was submitted
        if not symbol:
            return apology("missing symbol", 400)

        # Look up quote for symbol
        quote = lookup(symbol)

        # Ensure the symbol is correct
        if quote is None:
            return apology("invalid symbol", 400)

        # Ensure the shares is correct
        try:
            shares = int(shares)

            if shares < 1:
                raise ValueError()
        except ValueError:
            return apology("invalid shares", 400)

        # Get price
        price_per_share = quote["price"]

        # Query database for user shares
        rows = db.execute(
            """
            SELECT
                SUM(quote_shares) AS shares
            FROM
                transactions
            WHERE
                user_id = ?
                AND quote_symbol = ?
            """,
            user_id,
            symbol,
        )
        user_shares = rows[0]["shares"]

        if user_shares < shares:
            return apology("too many shares", 400)

        # Query database for user cash
        user_cash = db.execute(
            """
            SELECT
                cash
            FROM
                users
            WHERE id = ?
            """,
            user_id,
        )[0]["cash"]

        # Calculate updated cash
        updated_cash = user_cash + price_per_share * shares

        # Start transaction
        db.execute("BEGIN TRANSACTION")

        # Withdraw money from the user's account
        db.execute(
            """
            UPDATE users
            SET
                cash = :cash
            WHERE
                id = :id
            """,
            id=user_id,
            cash=updated_cash,
        )

        # Add a new transaction to the list of transactions
        db.execute(
            """
            INSERT INTO
                transactions (
                    user_id,
                    quote_name,
                    quote_symbol,
                    quote_shares,
                    quote_price
                )
            VALUES
                (
                    :user_id,
                    :quote_name,
                    :quote_symbol,
                    :quote_shares,
                    :quote_price
                )
            """,
            user_id=user_id,
            quote_name=quote["name"],
            quote_symbol=quote["symbol"],
            quote_shares=-shares,
            quote_price=price_per_share,
        )

        # End transaction
        db.execute("COMMIT")

        # Show success message
        flash("Sold!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        symbols = db.execute(
            """
            SELECT
                quote_symbol AS symbol
            FROM
                transactions
            WHERE
                user_id = ?
            GROUP BY
                quote_name
            """,
            user_id,
        )

        return render_template("sell.html", symbols=symbols)
