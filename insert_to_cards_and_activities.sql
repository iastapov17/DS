INSERT INTO cards(num, uid, bonusprogramm)
SELECT DISTINCT( c.num), up.id, c.bonusprogramm
FROM userr us join card c on us.usid = c.usid
join activity a on c.num = a.num
join route r ON fromr = departure AND tor = arrival
join flights f ON f.idr = r.idr AND f.flight = a.code
join list_flight l on l.id_flight = f.idf AND a.datee::date = l.date
join passengers_aircraft pa on l.id = pa.id_flight
join unique_passengers up on pa.id_people = up.id AND
                                us.fname = up.passengerfirstname AND
                                us.lname = up.passengerlastname;
-- ====================================

INSERT INTO activities(cid, idf, fare)
select cs.cid, lf.id, a.fare
from activity a join card c ON a.num = c.num
join cards cs ON c.num = cs.num
join unique_passengers up on cs.uid = up.id
join passengers_aircraft pa on up.id = pa.id_people
join list_flight lf on pa.id_flight = lf.id