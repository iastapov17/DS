-- ===================================
drop table cards, activities if exists;

CREATE TABLE cards(
    cid SERIAL NOT NULL PRIMARY KEY,
    num VARCHAR(15) NOT NULL,
    uid INT NOT NULL REFERENCES unique_passengers(id),
    bonusprogramm VARCHAR(25)
);

CREATE TABLE activities(
    aid SERIAL NOT NULL PRIMARY KEY,
    cid INT NOT NULL REFERENCES cards(cid),
    idf INT NOT NULL REFERENCES list_flight(id),
    fare VARCHAR(8)
);
