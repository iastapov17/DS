# coding=utf8
import PyPDF2
import re
import psycopg2
import json

conn = psycopg2.connect(database="ds", user="ruslan", host="localhost",
                        port="5432", password="ruslan")
cursor = conn.cursor()

route = r"(FROM:(.+))(TO:(.+))"
flight = r'(\d{2}) ([A-Z][a-z]{2})  -  (\d{2}) ([A-Z][a-z]{2})([\d\s]+)(\d{2}:\d{2}(\+\d)?)(\d{2}:\d{2}(\+\d)?)((([A-Z]{2}|[A-Z]\d|\d[A-Z])[0-9](\d{1,4})?(\*)?))(.{3})(\d+H\d+M)(Operated by:\s*\D+)?'
indexes = [0, 1, 2, 3, 4, 5, 7, 9, 14, 15, 16]


def get_data(reg, text, to):
    cursor.execute("SELECT idR FROM Route WHERE FromR = '{}' and ToR = '{}';".format(to[0], to[1]))
    idt = cursor.fetchall()[0][0]
    for i, v in enumerate(re.findall(reg, text)):
        print(i, [v[j] for j in indexes])
        cursor.execute("INSERT INTO Flights (Validity, Days, DepTime, ArrTime, Flight, Aircraft, Travel_Time,Operated_by, idR) \
                            VALUES ('{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', {});".format(
            v[0] + ' ' + v[1] + '-' + v[2] + ' ' + v[3],
            v[4].replace(' ', ''),
            v[5],
            v[7],
            v[9],
            v[14],
            v[15],
            v[16].split(':')[-1].replace(' ', '') if v[16] else "",
            idt))
        conn.commit()

    return True


def get_adr(reg, text):
    result = []
    # print(text)
    matches = re.finditer(reg, text)
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if groupNum % 2:
                result.append(match.group(groupNum)[-3:])
    print(result)
    if result:
        cursor.execute("INSERT INTO Route (FromR, ToR) \
                            VALUES ('{}', '{}');".format(result[0], result[1]))
        conn.commit()
    return result


def main(f):
    pl = open(f, 'rb')
    plread = PyPDF2.PdfFileReader(pl)
    for page in range(4, plread.getNumPages()):
        print("Page ", page)
        getpage = plread.getPage(page)
        text = getpage.extractText().replace('\n', '')
        text = text.split("ValidityDaysDepTimeArrTimeFlightAircraftTravelTime")
        if len(text) == 2:
            temp_to = get_adr(route, text[0])
            to = temp_to if temp_to else to
            get_data(flight, text[1], to)
        else:
            get_data(flight, text[0], to)


with open("Days.json", "r") as write_file:
    Days = json.load(write_file)

with open("Aircraft Types.json", "r") as write_file:
    Aircraft_Types = json.load(write_file)

for i, v in Days.items():
    cursor.execute("INSERT INTO Days (idD, value) \
                        VALUES ({}, '{}');".format(i, v))
    conn.commit()

for i, v in Aircraft_Types.items():
    cursor.execute("INSERT INTO AirType (idA, value) \
                        VALUES ('{}', '{}');".format(i, v))
    conn.commit()

for i in ['r1.pdf', 'l1.pdf']:
    main(i)
