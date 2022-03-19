/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS library_system (
  matric_number VARCHAR(9) NOT NULL ,
  email VARCHAR(256) NOT NULL,
  library VARCHAR(7) NOT NULL, CHECK (library IN ('CLB','SLB')),
  time_entered TIMESTAMPTZ DEFAULT Now(),
  time_exited TIMESTAMPTZ ,
  PRIMARY KEY(matric_number,email) );  --So that student can have multiple entries in the system where they entered at different times

CREATE TABLE IF NOT EXISTS student(
  student VARCHAR(9),
  email VARCHAR(256),
  FOREIGN KEY (student, email) REFERENCES library_system(matric_number,email)
  ON DELETE CASCADE DEFERRABLE
);

CREATE TABLE IF NOT EXISTS available(
	library VARCHAR(7) NOT NULL,
	level INT NOT NULL,
	total_seats INT NOT NULL,
	available_seats INT NOT NULL,
	PRIMARY KEY(library, level)
);
