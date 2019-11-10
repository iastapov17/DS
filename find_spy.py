import csv
import datetime


def check_flights(data):
    list_flights = []
    f = open('spy.txt', 'a')
    for i in data:
        tr_time = i['travel_time'].split('H')
        if len(tr_time) > 1:
            h = int(tr_time[0])
            m = int(tr_time[1].split('M')[0])
        else:
            h, m = (0, 0)
        list_flights.append(
            datetime.datetime.strptime(i['date'] + ' ' + i['deptime'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                hours=h, minutes=m))
    for i, v in enumerate(list_flights):
        for j, k in enumerate(list_flights):
            if k != v:
                if (k - v).days == 0:
                    if data[i]['tor'] != data[j]['fromr']:
                        tr_time = data[i]['travel_time'].split('H')
                        if len(tr_time) > 1:
                            h = int(tr_time[0])
                            m = int(tr_time[1].split('M')[0])
                        else:
                            h, m = (0, 0)
                        tr_time = data[j]['travel_time'].split('H')
                        if len(tr_time) > 1:
                            h1 = int(tr_time[0])
                            m1 = int(tr_time[1].split('M')[0])
                        else:
                            h1, m1 = (0, 0)

                        diff = (datetime.timedelta(hours=h1, minutes=m1) - datetime.timedelta(
                                hours=h, minutes=m)).seconds / 300
                        if diff != 1 and diff != 2:
                            f.write("Возможный шпион!" + '\n')
                            keys = data[i].keys()
                            string = ''
                            for key in keys:
                                string += key + ': ' + data[i][key] + '; '
                            f.write(string + '\n')
                            string = ''
                            for key in keys:
                                string += key + ': ' + data[j][key] + '; '
                            f.write(string + '\n')
                            f.write('\n')
    f.close()


def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    temp = []
    last = 0
    for j, line in enumerate(reader):
        if j == 0:
            last = line['id_people']
            temp.append(line)
            continue
        if last != line['id_people']:
            last = line['id_people']
            check_flights(temp)
            temp = [line]
        else:
            temp.append(line)


if __name__ == "__main__":
    with open("data.csv") as f_obj:
        csv_dict_reader(f_obj)
