
Database Creation:
------------------
create database authenticate;

use authenticate;


create table user(
	u_id int primary key auto_increment,
	u_name varchar(40) not null,
	email varchar(40) not null unique,
	password varchar(255) not null
	);

