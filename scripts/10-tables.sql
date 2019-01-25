CREATE TABLE characters (
	charid INT NOT NULL ,
	name TEXT ,
	PRIMARY KEY (charid)
);


CREATE TABLE films (
	id INT NOT NULL AUTO_INCREMENT ,
	charid INT NOT NULL ,
	title TEXT ,
	PRIMARY KEY (id)
);
