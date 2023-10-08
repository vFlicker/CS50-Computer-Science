**Find the crime scene report matching the date and location**

Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. Littering took place at 16:36. No known witnesses.

**Find interviews where transcripts mention the bakery**

- Ruth – Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
- Eugene – I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
- Raymond – As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

**Find people whose car's license plates left the parking lot shortly after the crime**

```
+---------+---------------+
|  name   | license_plate |
+---------+---------------+
| Vanessa | 5P2BI95       |
| Bruce   | 94KL13X       |
| Barry   | 6P58WS2       |
| Luca    | 4328GD8       |
| Sofia   | G412CB7       |
| Iman    | L93JTIZ       |
| Diana   | 322W7JE       |
| Kelsey  | 0NTHK55       |
+---------+---------------+
```

**Find people who withdrew money on Leggett Street**

```
+---------+----------------+-----------------+---------------+
|  name   |  phone_number  | passport_number | license_plate |
+---------+----------------+-----------------+---------------+
| Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
| Kaelyn  | (098) 555-1164 | 8304650265      | I449449       |
| Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
| Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
| Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
| Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
| Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
| Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
| Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
+---------+----------------+-----------------+---------------+
```

**Find people who had phone calls less than 60 seconds on 28.08.2021**

```
+---------+----------------+----------------+
|  name   |     caller     |    receiver    |
+---------+----------------+----------------+
| Sofia   | (130) 555-0289 | (996) 555-8899 |
| Kelsey  | (499) 555-9472 | (892) 555-8872 |
| Bruce   | (367) 555-5533 | (375) 555-8161 |
| Kelsey  | (499) 555-9472 | (717) 555-1342 |
| Taylor  | (286) 555-6063 | (676) 555-6554 |
| Diana   | (770) 555-1861 | (725) 555-3243 |
| Carina  | (031) 555-6622 | (910) 555-3251 |
| Kenny   | (826) 555-1652 | (066) 555-9701 |
| Benista | (338) 555-6650 | (704) 555-2131 |
+---------+----------------+----------------+
```

**Find the airport ID in Fiftyville**

```
+----+
| id |
+----+
| 8  |
+----+
```

**Find all flight IDs from the airport in Fiftyville on 29th July **

```
+----+
| id |
+----+
| 18 |
| 23 |
| 36 |
| 43 |
| 53 |
+----+
```

**Find passengers' passports for the earliest flight out of Fiftyville on 29th July**

```
+--------+-----------------+------------------------+
|  name  | passport_number | destination_airport_id |
+--------+-----------------+------------------------+
| Doris  | 7214083635      | 4                      |
| Sofia  | 1695452385      | 4                      |
| Bruce  | 5773159633      | 4                      |
| Edward | 1540955065      | 4                      |
| Kelsey | 8294398571      | 4                      |
| Taylor | 1988161715      | 4                      |
| Kenny  | 9878712108      | 4                      |
| Luca   | 8496433585      | 4                      |
+--------+-----------------+------------------------+
```

**Find the person who has been in all situations**

```
+-------+
| name  |
+-------+
| Bruce |
+-------+
```

**Find the accomplice**

```
+-------+
| name  |
+-------+
| Robin |
+-------+
```

**Find the city the thief escaped to**

```
+---------------+
|     city      |
+---------------+
| New York City |
+---------------+
```
