/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS NUS_system (
  matric_number VARCHAR(9) NOT NULL UNIQUE,
  email VARCHAR(256) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS library_system (
  matric_number VARCHAR(9) NOT NULL REFERENCES NUS_system(matric_number),
  email VARCHAR(256) NOT NULL REFERENCES NUS_system(email),
  library VARCHAR(7) NOT NULL,
  time_entered TIMESTAMPTZ DEFAULT Now(),
  time_exited TIMESTAMPTZ ,
  PRIMARY KEY(matric_number,email,time_entered)
);  --So that student can have multiple entries in the system where they entered at different times

CREATE TABLE IF NOT EXISTS student(
  matric_number VARCHAR(9) REFERENCES NUS_system(matric_number),
  email VARCHAR(256) REFERENCES NUS_system(email) ,
  library VARCHAR(7) NOT NULL REFERENCES available(library),
  Level INT NOT NULL REFERENCES available(level),
  time_entered TIMESTAMPTZ DEFAULT Now(),
  time_exited TIMESTAMPTZ ,
  PRIMARY KEY(matric_number,email,time_entered)
);

CREATE TABLE IF NOT EXISTS available(
	library VARCHAR(7) NOT NULL,
	level INT NOT NULL,
	available_seats INT NOT NULL CHECK(available_seats > -1 and available_seats<=total_seats),
	total_seats INT NOT NULL,
	PRIMARY KEY(library, level)
);
