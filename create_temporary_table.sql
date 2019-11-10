CREATE TABLE Pax
(
    idTicket serial,
    PaxSurname VARCHAR(30),
    PaxName VARCHAR(30),
    PaxPatr VARCHAR(30),
    PaxBirthDate VARCHAR(10), 
    DepartDate VARCHAR(10), 
    DepartTime VARCHAR(5),
    ArrivalDate VARCHAR(10),
    ArrivalTime VARCHAR(5),
    FlightCodeSh VARCHAR(10),
    Fromm VARCHAR(5),
    Dest VARCHAR(5),
    Code VARCHAR(24), 
    ETicket VARCHAR(6),
    TravelDoc VARCHAR(8),
    Seat VARCHAR(5),
    Meal VARCHAR(4),
    TrvClsFare CHAR(1),
    Baggage VARCHAR(12),
    PaxAdditionalInfo VARCHAR(22),
    Unkn1 VARCHAR(7),
    Unkn2 VARCHAR(12),
    AgentInfo VARCHAR(20)
);

drop table if exists activity, card, userr;

CREATE TABLE userr(
    usid INT NOT NULL PRIMARY KEY,
    fname VARCHAR(30),
    lname VARCHAR(30)
);

CREATE TABLE card(
    cid SERIAL NOT NULL PRIMARY KEY,
    num VARCHAR(15) NOT NULL UNIQUE,
    usid INT NOT NULL REFERENCES userr(usid),
    ctype VARCHAR(10),
    bonusprogramm VARCHAR(25)
);

CREATE TABLE activity(
    aid SERIAL NOT NULL PRIMARY KEY,
    num VARCHAR(15) REFERENCES card(num),
    astype VARCHAR(10),
    atype VARCHAR(10),
    code VARCHAR(10),
    datee VARCHAR(11),
    departure VARCHAR(5),
    arrival VARCHAR(5),
    fare VARCHAR(8)
);

select