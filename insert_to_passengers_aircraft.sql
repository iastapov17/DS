-- =======================================

-- insert into passengers_aircraft
INSERT INTO passengers_aircraft(id_flight, id_people, seat, ticket)
with t(id_flight, id_people, booking_code, ticket) as (
    select distinct l.id, u.id, left(code, 6), right(code, 16)
    from list_flight l
             join flights f on l.id_flight = f.idf
             join pax p ON l.date = p.departdate::date AND f.deptime = p.departtime::TIME and
                           f.flight = left(p.flightcodesh, 6)
             join unique_passengers u
                  ON CASE WHEN p.paxbirthdate = 'N/A' THEN '1970-01-01'::date else p.paxbirthdate::date end = u.passengerbirthdate::date AND
                     p.eticket || ' ' || p.traveldoc = u.passengerdocument
    where not l.id = 395608
)
    select * from t
    except
    (
        select p.id_flight, p.id_people, t.booking_code, t.ticket from passengers_aircraft p
        join t ON t.id_flight = p.id_flight AND t.id_people = p.id_people
    );

