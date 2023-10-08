import csv
from cs50 import SQL


def main():
    # Connect to the database
    db = SQL("sqlite:///roster.db")

    # Open the CSV file for reading
    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract data from the current row
            id, student_name, house, head = (
                row["id"],
                row["student_name"],
                row["house"],
                row["head"],
            )

            # Start transaction
            db.execute("BEGIN TRANSACTION")

            # Feel the 'students' table
            db.execute("INSERT INTO students (student_name) VALUES (?)", student_name)

            # Feel the 'houses' table
            db.execute(
                "INSERT OR IGNORE INTO houses (house, head) VALUES (?, ?)", house, head
            )

            # Feel the 'house_assignments' table
            db.execute(
                "INSERT INTO house_assignments (student_id, house_name) VALUES (?, ?)",
                id,
                house,
            )

            # End transaction
            db.execute("COMMIT")


main()
