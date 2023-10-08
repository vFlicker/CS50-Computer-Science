/* Find the crime scene report matching the date and location */
SELECT
  description
FROM
  crime_scene_reports AS c
WHERE
  c.year = 2021
  AND c.month = 07
  AND c.day = 28
  AND c.street = "Humphrey Street";

/* Find interviews where transcripts mention the bakery */
SELECT
  i.name,
  i.transcript
FROM
  interviews AS i
WHERE
  i.year = 2021
  AND i.month = 07
  AND i.day = 28
  AND i.transcript LIKE "%bakery%";

/* Find people whose car's license plates left the parking lot shortly after the crime */
SELECT
  p.name,
  l.license_plate
FROM
  bakery_security_logs AS l
  JOIN people AS p ON p.license_plate = l.license_plate
WHERE
  l.year = 2021
  AND l.month = 07
  AND l.day = 28
  AND l.hour = 10
  AND l.minute BETWEEN 15 AND 25
  AND l.activity = "exit";

/* Find people who withdrew money on Leggett Street */
SELECT
  p.name,
  p.phone_number,
  p.passport_number,
  p.license_plate
FROM
  atm_transactions AS t
  JOIN bank_accounts AS a ON t.account_number = a.account_number
  JOIN people AS p ON a.person_id = p.id
WHERE
  t.year = 2021
  AND t.month = 07
  AND t.day = 28
  AND t.atm_location = "Leggett Street";

/* Find people who had phone calls less than 60 seconds on 28.08.2021 */
SELECT
  p2.name,
  p1.caller,
  p1.receiver
FROM
  phone_calls AS p1
  JOIN people AS p2 ON p1.caller = p2.phone_number
WHERE
  p1.year = 2021
  AND p1.month = 07
  AND p1.day = 28
  AND p1.duration < 60;

/* Find the airport ID in Fiftyville */
SELECT
  a.id
FROM
  airports AS a
WHERE
  a.city = "Fiftyville";

/* Find all flight IDs from the airport in Fiftyville on 29th July */
SELECT
  f.id
FROM
  flights AS f
WHERE
  f.day = 29
  AND f.origin_airport_id = 8;

/* Find passengers' passports for the earliest flight out of Fiftyville on 29th July */
SELECT
  p2.name,
  p1.passport_number,
  f.destination_airport_id
FROM
  passengers AS p1
  JOIN flights AS f ON p1.flight_id = f.id
  JOIN airports AS a ON f.origin_airport_id = a.id
  JOIN people AS p2 ON p1.passport_number = p2.passport_number
WHERE
  f.day = 29
  AND a.city = "Fiftyville"
ORDER BY
  f.hour,
  f.minute
LIMIT
  8;

/* Find the person who has been in all situations */
SELECT
  p1.name
FROM
  people AS p1
  JOIN bakery_security_logs AS l ON p1.license_plate = l.license_plate
  JOIN bank_accounts AS a ON p1.id = a.person_id
  JOIN atm_transactions AS t ON a.account_number = t.account_number
  JOIN phone_calls AS p2 ON p1.phone_number = p2.caller
WHERE
  l.year = 2021
  AND l.month = 07
  AND l.day = 28
  AND l.hour = 10
  AND l.minute >= 15
  AND l.minute <= 25
  AND l.activity = "exit"
  AND p2.year = 2021
  AND p2.month = 07
  AND p2.day = 28
  AND p2.duration < 60
  AND t.year = 2021
  AND t.month = 07
  AND t.day = 28
  AND p1.phone_number IN (
    SELECT
      p2.phone_number
    FROM
      passengers AS p1
      JOIN flights AS f ON p1.flight_id = f.id
      JOIN airports AS a ON f.origin_airport_id = a.id
      JOIN people AS p2 ON p1.passport_number = p2.passport_number
    WHERE
      f.day = 29
      AND a.city = "Fiftyville"
    ORDER BY
      f.hour,
      f.minute
    LIMIT
      8
  );

/* Find the accomplice */
SELECT
  p.name
FROM
  people AS p
WHERE
  p.phone_number = "(375) 555-8161";

/* Find the city the thief escaped to */
SELECT
  a.city
FROM
  airports AS a
WHERE
  a.id = 4;