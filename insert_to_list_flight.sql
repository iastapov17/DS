-- Insert into
INSERT INTO list_flight(date, id_flight)
select p.departdate::date,f.idf
FROM pax p join flights f ON f.deptime = p.departtime::Time AND f.deptime = p.departtime::TIME and f.flight = left(p.flightcodesh, 6)
    except (
         select l.date, id_flight
         FROM list_flight l
             join flights f on l.id_flight = f.idf
             join pax p ON l.date = p.departdate::date AND f.deptime = p.departtime::TIME and
             f.flight = left(p.flightcodesh, 6)
    );

