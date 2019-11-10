import csv


def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    f = open('spy_1.txt', 'a')
    temp = {}
    for j, line in enumerate(reader):
        if line['passengerdocument'] == '':
            continue
        if line['passengerbirthdate'] == '1970-01-01':
            continue
        if line['passengerdocument'] in temp:
            for i in temp[line['passengerdocument']]:
                if i['id_people'] != line['id_people'] and line['passengerbirthdate'] != i['passengerbirthdate']:
                    f.write("Возможный шпион!" + '\n')
                    keys = i.keys()
                    string = ''
                    for key in keys:
                        string += key + ': ' + i[key] + '; '
                    f.write(string + '\n')
                    string = ''
                    for key in keys:
                        string += key + ': ' + line[key] + '; '
                    f.write(string + '\n')
                    f.write('\n')
            temp[line['passengerdocument']].append(line)
        else:
            temp[line['passengerdocument']] = [line]

if __name__ == "__main__":
    with open("data.csv") as f_obj:
        csv_dict_reader(f_obj)
