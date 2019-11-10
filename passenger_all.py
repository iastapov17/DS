import csv
import psycopg2


# create tmp table
def init():
    try:
        conn = psycopg2.connect("dbname='ds' user='lizzie' host='94.250.250.51' password='lizzie'")
    except Exception as e:
        print(e)
    return conn


def main():
    conn = init()
    cur = conn.cursor()
    with open('/home/elizabeth/Загрузки/midsem/BoardingData.csv', 'r') as f:
        # skip title
        f.readline()

        s = f.readline()
        while s:
            data = s.split(";")
            cur.execute("""INSERT INTO passengers_liza VALUES(DEFAULT, '{}', '{}', '{}', '{}'
                    , '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                        .format(data[0],
                                data[1],
                                data[2],
                                data[3],
                                data[4],
                                data[5],
                                data[6],
                                data[7],
                                data[8],
                                data[9],
                                data[10],
                                data[11],
                                data[12],
                                data[13]))
            conn.commit()
            s = f.readline()


main()
