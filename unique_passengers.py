import csv
import psycopg2
import re

f = ''


def init():
    global f
    f = open("liza_log.txt", "w")
    try:
        conn = psycopg2.connect("dbname='ds' user='lizzie' host='94.250.250.51' password='lizzie'")
    except Exception as e:
        print(e)
    return conn


# поиск обратного маршрута
def find_return(direct_number):
    conn = init()
    cur = conn.cursor()
    num = int(re.findall('\d+', direct_number)[0])
    letters = re.findall('[A-Z]+', direct_number)[0]
    if num % 2 == 0:
        num += 1
    else:
        num -= 1
    flight = letters + str(num);
    cur.execute("SELECT fromr, tor FROM flights join route using(idr) WHERE flight='{}' limit(1)".format(flight))
    res = cur.fetchall()
    if len(res):
        cur.execute("INSERT INTO route VALUES(DEFAULT, '{}', '{}', TRUE)".format(res[0][1], res[0][0]))
        cur.execute("SELECT idr FROM route ORDER BY idr DESC LIMIT 1")
        res = cur.fetchall[0][0]
        return res
    else:
        return None


def main():
    conn = init()
    cur = conn.cursor()

    current_position = 0

    cur.execute("SELECT count(*) FROM passengers_liza")
    qty = cur.fetchall()[0][0]

    while current_position < qty:
        cur.execute("SELECT * FROM passengers_liza LIMIT(100) OFFSET {}".format(current_position))
        passengers = cur.fetchall()
        for i in passengers:
            cur.execute("SELECT * FROM flights WHERE flight='{}'".format(i[12]))
            current_number = cur.fetchall()
            # поиск маршрута
            if not len(current_number):
                route = find_return(i[12])
            else:
                route = current_number[0][6]
            if not route:
                print("not route")
                break

            # поиск нужного рейса
            cur.execute("SELECT * FROM flights WHERE flight='{}' and deptime = '{}'".format(i[12], i[11]))
            current_flight = cur.fetchall()
            if not len(current_flight):
                cur.execute("INSERT INTO flights VALUES (DEFAULT, null, '{}', '{}', null, null, {}, true)"
                            .format(i[11], i[12], route))
                print("INSERT INTO flights VALUES (DEFAULT, null, '{}', '{}', null, null, {}, true)"
                            .format(i[11], i[12], route))
                cur.execute("SELECT idf FROM flights ORDER BY idf DESC LIMIT 1")
                current_flight = cur.fetchall()[0][0]
            else:
                current_flight = current_flight[0][0]

            # поиск нужного рейса и даты
            cur.execute(
                "SELECT id FROM list_flight WHERE id_flight = {} and date = '{}'".format(current_flight, i[10]))
            idl = cur.fetchall()
            if not len(idl):
                cur.execute("INSERT INTO list_flight VALUES (DEFAULT, '{}', {})".format(i[10], current_flight))
                print("INSERT INTO list_flight VALUES (DEFAULT, '{}', {})".format(i[10], current_flight))
                cur.execute("SELECT id FROM list_flight ORDER BY id DESC LIMIT 1")
                idl = cur.fetchall()[0][0]
            else:
                idl = idl[0][0]
            cur.execute(
                "SELECT id FROM unique_passengers WHERE passengerfirstname='{}' and passengerlastname='{}' and passengerbirthdate='{}' and passengerdocument='{}'"
                .format(i[1], i[3], i[5], i[6]))
            idp = cur.fetchall()
            if not len(idp):
                print("not passenger")
                break
            idp = idp[0][0]
            # вставка пассажира рейса
            cur.execute("SELECT * FROM passengers_aircraft WHERE id_flight={} and id_people={}".format(idl, idp))
            if not len(cur.fetchall()):
                cur.execute("INSERT INTO passengers_aircraft VALUES({}, {}, null, '{}', '{}', null)"
                            .format(idl, idp, i[7], i[8]))
                print("INSERT INTO passengers_aircraft VALUES({}, {}, null, '{}', '{}', null)"
                            .format(idl, idp, i[7], i[8]))
        current_position += 100
        f.write(str(current_position))
        f.write("\n")
        conn.commit()


main()
f.close()
