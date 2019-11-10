SELECT u1.passengerfirstname,
       u1.passengerlastname,
       u1.passengerdocument,
       u1.passengerbirthdate,
       u2.passengerbirthdate,
       u2.passengerdocument,
       u2.passengerfirstname,
       u2.passengerlastname
    FROM unique_passengers u1, unique_passengers u2
        WHERE u1.passengerdocument = u2.passengerdocument AND
         u1.passengerbirthdate <> u2.passengerbirthdate and not u1.id < u2.id
    ORDER BY u1.passengerfirstname, u2.passengerlastname;