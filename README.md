# Data Science
Your skills in Data Science became well recognized around the world. And you had been recruited by MI6 as external consultant for helping to find potential "The Russian Spies" among frequent flyers. For the first task you should to perform some data merging and cleaning in dataset obtained from different sources as booking sites, frequent flyiers forums, ticket agencies, etc about flights of several suspicious Russian citizens. Download following dataset, merge and clean them, and try to recover some valuable information about travel patterns.

### Файлы:
- ***DataBase.sql*** - Скрипт создания базы данных.
- ***main.py*** - Парсинг pdf файла.  
- ***find_spy.py*** - Код для поиска подозрительных личностей.
- ***find_spy.py*** - Код для поиска подозрительных личностей.
- ***spy.txt*** - Подозрительные личности.
- ***spy_1.txt*** - Подозрительные личности.
- ***data.csv.zip*** - Информация о билетах.
- ***parse_yaml.py*** - Считывание информации из файла yaml и запись в словарь.
- ***parse_xlsx.py*** - Считывание информации из файла xlsx и запись в словарь.
- ***check_info_in_base.py*** - Вставка информации о билетах в базу.
- ***passenger_all.py*** - Временная таблица из csv.
- ***read_json.py*** - Обработка frequent flyer.
- ***unique_passengers.py*** - Выделение пассажиров конкретного рейса.
### Порядок занесения данных из xml и tab файлов  

- ***(tab_parse.py, create_temporary_table.sql)*** - Разбор таб-файла(билеты). В исходном файле данные разделены табуляциями, что-то может отсутствовать. Вставка во временную талицу pax реализована следующим образом: проверяем текущий атрибут, если не соотвествует выбранному для этой колонки паттерну, значит атрибут принадлежит одной из следующих колонок.

- ***(xml_parse.go, create_temporary_table.sql)*** - Разбор хмл. При помощи методов из библиотеки для разбора xml исходный файл парсится в структуру => все значения из файла добавляются в соответствующие поля структуры. Из заполненной структуры во временные таблицы пользователей userr, их карт card и программ лояльности activity асинхронно добавляются данные.

- ***(insert_to_inuque_passengers.sql, insert_to_list_flight.sql)*** - Перенос данных из временной таблицы билетов предполагал занесение новых маршрутов и полетов из расписания (новые записи отсутствовали), а так же новых уникальных пассажирова и пассажиров полетов. Данные успешно добавлены.  

- ***(create_cards_activities.sql, insert_to_cards_and_activities.sql)*** -  Перенос данных из card и activity в новые таблицы cards и activities, отличия данных во временных и итоговых таблицах состоят в замене ключей из временной таблицы userr ключами из unique_passengers. Сформиованна конечная структура.  

- ***(select_spy_from_table.sql)*** - Вывод пассажиров с одинаковыми паспортами и разными датами рождения.  
