import json
import psycopg2
from pprint import PrettyPrinter

pprint = PrettyPrinter(indent=4).pprint


def init():
    try:
        conn = psycopg2.connect(dbname='ds', user='lizzie', host='94.250.250.51', password='lizzie')
    except Exception as e:
        print(e)
    return conn


def main():
    conn = init()
    cur = conn.cursor()
    with open("/home/elizabeth/Загрузки/midsem/FrequentFlyerForum-Profiles.json", "r") as read_file:
        data = json.load(read_file)

    profiles = data.get('Forum Profiles')
    qty = len(profiles)
    c = 0
    while c < qty:
        i = profiles[c]
        print(c)
        c += 1
        flights = []
        nums = []
        for f in i.get('Registered Flights'):
            arr = f.get('Arrival').get('Airport')
            dep = f.get('Departure').get('Airport')
            del f['Codeshare']
            del f['Arrival']
            del f['Departure']
            f['from'] = arr
            f['to'] = dep
            flights.append(f)

        global uid
        global card
        uid = -1

        programs = i.get('Loyality Programm')
        if i.get('Real Name').get('Last Name') is None:
            for p in programs:
                num = p.get('programm') + p.get('Number')
                cur.execute("SELECT * FROM cards WHERE num = '{}' ".format(num))
                card = cur.fetchall()
                if len(card) != 0:
                    uid = card[0][2]
                    break
        else:
            # ищем человека с заданными именем и фамилией в таблице пассажиров
            fname = i.get('Real Name').get('First Name')
            fname = fname.replace("'", '').replace("SHCH", "SH").replace("YU", "IU").replace("YA", "IA") \
                .replace("AY", "AI").replace("IY", "II").replace("EY", "EI").replace('X', 'KS')
            lname = i.get('Real Name').get('Last Name')
            lname = lname.replace("'", '').replace("SHCH", "SH").replace("YU", "IU").replace("YA", "IA") \
                .replace("AY", "AI").replace("IY", "II").replace("EY", "EI").replace('X', 'KS')
            cur.execute(
                "SELECT f.flight, l.date, p.id FROM unique_passengers p JOIN passengers_aircraft a ON p.id=a.id_people "
                "JOIN list_flight l ON l.id=a.id_flight "
                "JOIN flights f ON l.id_flight = f.idf "
                "WHERE passengerfirstname = '{}' and passengerlastname = '{}'"
                    .format(fname, lname))
            found_flights = cur.fetchall()
            for ff in found_flights:
                for f in flights:
                    if ff[0] == f['Date'] and ff[1] == f['Flight']:
                        uid = ff[2]
                        break
                if uid != -1:
                    break

        if uid == -1:
            continue
        # если нет имени в ff и записей с именем в программах, то ничего не делаем с записью
        else:
            for p in programs:
                num = p.get('programm') + p.get('Number')
                nums.append(num)
                cur.execute("SELECT * FROM cards WHERE num = '{}' ".format(num))
                card = cur.fetchall()
                if len(card) == 0:
                    # запись отсутсвующих программ лояльности пассажира
                    cur.execute("INSERT INTO cards VALUES(DEFAULT, '{}', {}, null)".format(num, uid))
                    conn.commit()
        for f in flights:
            # поиск соответствия рейса программе лояльности
            cur.execute("SELECT yaml.number FROM yaml WHERE yaml.date = '{}' and yaml.flight = '{}'"
                        .format(f['Date'], f['Flight']))
            found_nums = cur.fetchall()
            if len(found_nums) == 0:
                break
            num = set(nums).intersection(set([num[0] for num in found_nums]))
            num = num.pop()
            cur.execute("SELECT cid FROM cards WHERE uid = '{}' and num = '{}'".format(uid, num))
            card = cur.fetchall()
            if len(card) == 0:
                cur.execute("INSERT INTO cards VALUES(DEFAULT, '{}', {}, null)".format(num, uid))
                cur.execute("SELECT cid FROM cards WHERE uid = '{}' and num = '{}'".format(uid, num))
                card = cur.fetchall()
                conn.commit()
            card = card[0][0]
            # поиск нужного рейса
            cur.execute("SELECT l.id FROM list_flight l join flights f ON l.id_flight = f.idf "
                        "JOIN passengers_aircraft p ON p.id_flight = l.id "
                        "WHERE p.id_people = {} and l.date = '{}' and f.flight = '{}'"
                        .format(uid, f['Date'], f['Flight']))
            list_flight = cur.fetchall()
            if len(list_flight) == 0:
                break
            list_flight = list_flight[0][0]
            cur.execute("INSERT INTO activities VALUES(DEFAULT, {}, {})".format(card, list_flight))
            conn.commit()


main()
