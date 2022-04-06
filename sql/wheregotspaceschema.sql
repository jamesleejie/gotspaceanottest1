/*******************

  Create the schema

********************/
CREATE TABLE IF NOT EXISTS faculty (
  faculty VARCHAR(64) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS department (
  department VARCHAR(64) PRIMARY KEY,
  faculty VARCHAR(64) REFERENCES faculty(faculty)
);

CREATE TABLE IF NOT EXISTS NUS_system (
  matric_number VARCHAR(9) NOT NULL UNIQUE,
  email VARCHAR(256) NOT NULL UNIQUE,
  student_department VARCHAR(64) NOT NULL REFERENCES department(department),
  student_year INT NOT NULL,
  hall BIT 
  
);

CREATE TABLE IF NOT EXISTS library_system (
  matric_number VARCHAR(9) NOT NULL REFERENCES NUS_system(matric_number),
  email VARCHAR(256) NOT NULL REFERENCES NUS_system(email),
  library VARCHAR(7) NOT NULL,
  time_entered TIMESTAMPTZ DEFAULT Now(),
  time_exited TIMESTAMPTZ DEFAULT Now(),
  PRIMARY KEY(matric_number,email,time_entered)
);  --So that student can have multiple entries in the system where they entered at different times


CREATE TABLE IF NOT EXISTS available(
	library VARCHAR(7) NOT NULL,
	level INT NOT NULL,
	available_seats INT NOT NULL CHECK(available_seats > -1 and available_seats<=total_seats),
	total_seats INT NOT NULL,
	PRIMARY KEY(library, level)
);


CREATE TABLE IF NOT EXISTS student(
  matric_number VARCHAR(9) REFERENCES NUS_system(matric_number),
  email VARCHAR(256) REFERENCES NUS_system(email) ,
  library VARCHAR(7) NOT NULL,
  Level INT NOT NULL,
  time_entered TIMESTAMPTZ DEFAULT Now(),
  time_exited TIMESTAMPTZ DEFAULT Now(),
  FOREIGN KEY(library,level) REFERENCES available(library,level),	
  PRIMARY KEY(matric_number,email,time_entered)
);


