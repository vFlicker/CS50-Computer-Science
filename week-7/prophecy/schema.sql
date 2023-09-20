DROP TABLE IF EXISTS students;

CREATE TABLE
  students (
    id INTEGER,
    student_name VARCHAR(255),
    PRIMARY KEY (id)
  );

DROP TABLE IF EXISTS houses;

CREATE TABLE
  houses (
    house VARCHAR(255),
    head VARCHAR(255),
    PRIMARY KEY (house)
  );

DROP TABLE IF EXISTS house_assignments;

CREATE TABLE
  house_assignments (
    student_id INTEGER,
    house_name VARCHAR(255),
    PRIMARY KEY (student_id, house_name),
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (house_name) REFERENCES houses (house)
  );