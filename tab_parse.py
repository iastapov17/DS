#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from psycopg2 import connect
import csv
import sys


translit = {
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Е": "E",
    "Ё": "E",
    "Ж": "ZH",
    "З": "Z",
    "И": "I",
    "Й": "I",
    "К": "K",
    "Л": "L",
    "М": "M",
    "Н": "N",
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "У": "U",
    "Ф": "F",
    "Х": "KH",
    "Ц": "TS",
    "Ч": "CH",
    "Ш": "SH",
    "Щ": "SH",
    "Ъ": "",
    "Ы": "Y",
    "Ь": "",
    "Э": "E",
    "Ю": "IU",
    "Я": "IA",
}
conn = connect(dbname='ds',
                user='denis', 
                password='denis', 
                host='94.250.250.51',
                port='5432')
print("Database opened successfully")
cur = conn.cursor()
a = False
with open("Sirena-export-fixed.tab", "r", encoding="utf8") as tsv:
    bad_lines = []
    bad_cols = []
    agents = {'Aerobilet', 'Aeroflot', 'Tickets.ru', 'KupiBilet', 'Kiwi.com', 'OneTwoTrip', 'Go2See', 'OZON.travel', 'City.Travel', 'Travelgenio', 'eDreams', 'trip.ru'}
    for line in tsv.readlines():
        line = line.split()
        if not a:
            a = True
            continue

        col = ["PaxSurname", "PaxName"]
        line[0] = ''.join([translit[i] for i in line[0].upper()])
        line[1] = ''.join([translit[i] for i in line[1].upper()])
        ci = 2
        if line[ci].find('1') > -1 or line[ci].find('2') > -1 or line[ci].lower().find('n/a') > -1:
            ci += 1
            col += ["PaxBirthDate"]
        else:
            ci += 2
            col += ["PaxPatr", "PaxBirthDate"]
            line[2] = ''.join([translit[i] for i in line[2].upper()])
        ci += 11
        col += ["DepartDate", "DepartTime", "ArrivalDate", "ArrivalTime", "FlightCodeSh", "Fromm", "Dest", "Code", "ETicket", "TravelDoc", "Seat"]

        if line[ci].find('ML') > -1:
            ci += 1
            col += ["Meal"]
        ci += 2
        col += ["TrvClsFare", "Baggage"]
        if len(line) > ci:
            if line[ci].find('FF') < 0 and line[ci] not in agents:
                ci += 1
                col += ["PaxAdditionalInfo"]
                while len(line) > ci and line[ci].find('FF') < 0 and line[ci] not in agents:
                        line[ci - 1] += ' ' + line.pop(ci)
            if len(line) > ci:
                if line[ci].find('FF') > -1:
                    ci += 2
                    col += ["Unkn1", "Unkn2"]
                if len(line) > ci: 
                    col += ["AgentInfo"]
                    agents.add(line[ci])
        if len(col) != len(line):
            bad_cols += [col]
            bad_lines += [line]
            continue
        col, line = ','.join(col), '\'' + '\', \''.join(line) + '\''
        print(col)
        print(line)
        cur.execute("""INSERT INTO Pax({}) VALUES ({});""".format(col, line))

    print("Bad data")
    for i in range(len(bad_cols)):
        print(bad_cols[i])
        print(bad_lines[i])
conn.commit() 

print("Finished")