=======================================
-- Insert into unique_passengers

INSERT INTO unique_passengers(passengerfirstname, passengersecondname, passengerlastname, passengerbirthdate, passengerdocument)
select paxsurname,
           paxpatr,
           paxname,
           CASE WHEN paxbirthdate = 'N/A' THEN '1970-01-01'::date else paxbirthdate::date end,
           eticket || ' ' || traveldoc
    from pax
        except (select passengerfirstname, passengersecondname, passengerlastname, passengerbirthdate, passengerdocument
                from unique_passengers);