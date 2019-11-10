
create table if not exists unique_passengers
(
	id serial not null
		constraint pk
			primary key,
	passengerfirstname varchar(30),
	passengersecondname varchar(30),
	passengerlastname varchar(30),
	passengersex integer,
	passengerbirthdate date,
	passengerdocument varchar(11),
	"foreign" boolean
);


create table if not exists route
(
	idr serial not null
		constraint route_ruslan_pkey
			primary key,
	fromr char(3) not null,
	tor char(3) not null,
	"foreign" boolean
);

create table if not exists flights
(
	idf serial not null
		constraint pkk
			primary key,
	days varchar(7),
	deptime time,
	flight varchar(10),
	aircraft varchar(10),
	travel_time varchar(10),
	idr integer
		constraint flights_route_idr_fk
			references route,
	"foreign" boolean
);

create table if not exists list_flight
(
	id serial not null
		constraint list_flight_pkey
			primary key,
	date date,
	id_flight integer
		constraint list_flight_flights_idf_fk
			references flights
);

create table if not exists passengers_aircraft
(
	id_flight integer not null
		constraint passengers_aircraft_list_flight_id_fk
			references list_flight,
	id_people integer not null
		constraint passengers_aircraft_unique_passengers_id_fk
			references unique_passengers,
	seat text,
	booking_code text,
	ticket text,
	sequence text,
	constraint tmm_pk
		primary key (id_people, id_flight)
);

create table if not exists cards
(
	cid serial not null
		constraint cards_pkey
			primary key,
	num varchar(15) not null,
	uid integer not null
		constraint cards_uid_fkey
			references unique_passengers,
	bonusprogramm varchar(25)
);

create table if not exists activities
(
	aid serial not null
		constraint activities_pkey
			primary key,
	cid integer not null
		constraint activities_cid_fkey
			references cards,
	idf integer not null
		constraint activities_idf_fkey
			references list_flight,
	fare varchar(8)
);


create table if not exists invalid_docs
(
	series varchar(4) not null,
	number varchar(6) not null
);

