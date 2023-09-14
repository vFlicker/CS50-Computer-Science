import csv
import requests

DAYS_IN_WEEK = 7


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    new_cases = dict()
    previous_cases = dict()

    for row in reader:
        state = row["state"]
        cases = int(row["cases"])

        # Initialize lists for new cases if not already present
        new_cases.setdefault(state, [])
        previous_cases.setdefault(state, 0)

        # Calculate new cases for the current day
        new_cases[state].append(cases - previous_cases[state])

        if len(new_cases[state]) > DAYS_IN_WEEK * 2:
            new_cases[state].pop(0)

        previous_cases[state] = cases

    return new_cases


# Calculate and print out seven day average for given state
def comparative_averages(new_cases, states):
    for state in states:
        current_week = new_cases[state][-DAYS_IN_WEEK:]
        previous_week = new_cases[state][:DAYS_IN_WEEK]

        current_week_average = sum(current_week) / DAYS_IN_WEEK
        previous_week_average = sum(previous_week) / DAYS_IN_WEEK

        diff = current_week_average - previous_week_average

        if previous_week_average != 0:
            percent = (diff / previous_week_average) * 100
        else:
            percent = 0

        trend = "an increase" if diff > 0 else "a decrease"

        print(
            f"{state} had a 7-day average of {current_week_average:.0f} and {trend} of {percent:.0f}%."
        )


main()
