import psycopg2
from re import findall
from yaml import load, Loader


conn = psycopg2.connect(dbname='ds', user='roman',
                        password='verepa40', host='94.250.250.51')
cursor = conn.cursor()


def get_strange_info():
    with open("/home/roman/Загрузки/Airlines/SkyTeam-Exchange.yaml", 'r') as f:
        text = f.read()
        days = findall(r"'.{10}'[^']*", text)
        data = []
        i = 0

        for day in days:
            yaml_data = load(day, Loader=Loader)
            date = list(yaml_data.keys())[0]
            flights = list(yaml_data[date].items())

            for flight in flights:
                num, info = flight
                fr = info['FROM']
                to = info['TO']
                ff = info['FF']
                for freqflir in ff.items():
                    fb, fb_info = freqflir[0], freqflir[1]
                    fare = fb_info['FARE']
                    cursor.execute("INSERT INTO yaml VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(date, num, fb, fare, fr, to))
            i += 1
            if i % 10 == 0:
                conn.commit()
                print(i / len(days))


get_strange_info()