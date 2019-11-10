import psycopg2
import json
from os import listdir
from os.path import isfile, join
from parse_yaml import get_strange_info
from parse_xlsx import get_flight_ticket


find_flight = "SELECT * FROM flights WHERE flight='{}' AND deptime='{}'"
find_people = "SELECT * FROM unique_passengers WHERE passengerfirstname='{}' AND passengerlastname='{}'"

conn = psycopg2.connect(dbname='ds', user='roman',
                        password='verepa40', host='94.250.250.51')
cursor = conn.cursor()


def add_people_in_flight(row):
    id_people = check_people(row)
    if not id_people:
        add_people_in_base(row)
        id_people = check_people(row)[0]
    else:
        id_people = id_people[0]

    cursor.execute(find_flight.format(row["Flight"], row["Time"]))
    id_flight = cursor.fetchall()
    if not id_flight:
        add_flight_in_base(row)
        cursor.execute(find_flight.format(row["Flight"], row["Time"]))
        id_flight = cursor.fetchall()[0][0]
    else:
        id_flight = id_flight[0][0]

    query = "SELECT * FROM list_flight WHERE id_flight={} AND date='{}'"
    cursor.execute(query.format(id_flight, row["Date"]))
    flight = cursor.fetchall()

    if not flight:
        add_flight_in_list(row)
        query = "SELECT * FROM list_flight WHERE id_flight={} AND date='{}'"
        cursor.execute(query.format(id_flight, row["Date"]))
        flight = cursor.fetchall()[0][0]
    else:
        flight = flight[0][0]

    q = "SELECT * FROM passengers_aircraft WHERE id_flight={} AND id_people={}"
    cursor.execute(q.format(flight, id_people))
    res = cursor.fetchall()
    if res:
        return

    query_insert = "INSERT INTO passengers_aircraft VALUES ({}, {}, '{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL)"
    cursor.execute(query_insert.format(flight, id_people, row["Seat"], row["PNR"], row["Ticket"], row["Sequence"]))
    conn.commit()


def add_flight_in_list(row):
    cursor.execute(find_flight.format(row["Flight"], row["Time"]))
    id_flight = cursor.fetchall()[0][0]

    query = "INSERT INTO list_flight VALUES (DEFAULT, '{}', {})"
    cursor.execute(query.format(row["Date"], id_flight))
    conn.commit()


def add_flight_in_base(row):
    query_r = "SELECT * FROM route WHERE fromr='{}' AND tor='{}'"
    cursor.execute(query_r.format(row["From_red"], row["To_red"]))
    result = cursor.fetchall()
    if result:
        route = result[0][0]
    else:
        query_fr = "INSERT INTO route VALUES (DEFAULT, '{}', '{}', TRUE)"
        cursor.execute(query_fr.format(row["From_red"], row["To_red"]))
        conn.commit()
        cursor.execute(query_r.format(row["From_red"], row["To_red"]))
        result = cursor.fetchall()
        route = result[0][0]

    query = "INSERT INTO flights VALUES (DEFAULT, 'DNTKnow', 'WNNull', '{}', '99:99', '{}', '-', '-', '-', '{}', TRUE)"
    cursor.execute(query.format(row["Time"], row["Flight"], route))
    conn.commit()


def add_people_in_base(row):
    secname = row["Secname"] if 'Secname' in row else ""
    query = "INSERT INTO unique_passengers VALUES (DEFAULT, '{}', '{}', '{}', {}, NULL, NULL, TRUE)"
    cursor.execute(query.format(row["Name"], secname, row["Surname"], row["Sex"]))
    conn.commit()


def check_people(row):
    if 'Secname' in row:
        query = find_people
        cursor.execute(query.format(row["Name"], row["Surname"]))
        result = cursor.fetchall()
        if result:
            for res in result:
                if len(res[2]) > 1 and row["Secname"][0] == res[2][0]:
                    return res
        else:
            cursor.execute(query.format(row["Surname"], row["Name"]))
            result = cursor.fetchall()
            if result:
                for res in result:
                    if len(res[2]) > 1 and row["Secname"][0] == res[2][0]:
                        return res
    else:
        cursor.execute(find_people.format(row["Name"], row["Surname"]))
        result = cursor.fetchall()
        if result:
            return result[0]

        cursor.execute(find_people.format(row["Surname"], row["Name"]))
        result = cursor.fetchall()
        if result:
            return result[0]
    return False


def check_flight_and_people(people=False, ticket=False, flight=False, passengers=False):
    path = "/home/roman/Загрузки/Airlines/passdot"
    files = [f for f in listdir(path) if isfile(join(path, f))]

    #files = ["YourBoardingPassDotAero-2017-02-09.xlsx"]
    for file in files[141:]:
        for row in get_flight_ticket(file):

            if flight:
                add_flight_in_list(row)

            if ticket:
                cursor.execute(find_flight.format(row["Flight"], row["Time"]))
                records = cursor.fetchall()
                if not records:
                    add_flight_in_base(row)

            if people:
                result = check_people(row)
                if not result:
                    add_people_in_base(row)

            if passengers:
                add_people_in_flight(row)

    cursor.close()
    conn.close()


check_flight_and_people(passengers=True)
# check_flight_and_people(flight=True)
# check_flight_and_people(passengers=True)
