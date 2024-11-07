DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS scan;
DROP TABLE IF EXISTS share;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  profession TEXT NOT NULL
);

CREATE TABLE scan (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  doctor_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  model TEXT NOT NULL,
  firstName TEXT NOT NULL,
  secondName TEXT NOT NULL,
  age INTEGER NOT NULL,
  gender INTEGER NOT NULL,
  symptoms TEXT,
  input_img NVARCHAR NOT NULL,
  output_res NVARCHAR NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (doctor_id) REFERENCES uesr (id)
);

CREATE TABLE share (
  share_id INTEGER PRIMARY KEY AUTOINCREMENT,
  scan_id INTEGER NOT NULL,
  og_doctor_id INTEGER NOT NULL,
  og_doctor_name TEXT NOT NULL,
  firstName TEXT NOT NULL,
  secondName TEXT NOT NULL,
  created TIMESTAMP NOT NULL,
  output_res TEXT NOT NULL,
  end_doctor_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (scan_id) REFERENCES scan (id),
  FOREIGN KEY (og_doctor_id) REFERENCES user (id),
  FOREIGN KEY (end_doctor_id) REFERENCES user (id)
);