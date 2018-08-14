create schema FinalProject;

use finalproject;

create table Files (
	id INT,
    filename VARCHAR(45),
    sha1 CHAR(40),
    modified DATETIME,
    bin LONGBLOB,
	primary key (id)
);