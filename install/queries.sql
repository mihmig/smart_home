-- Дверь туалета
SELECT left(datetime,10),count(*) from `0x00124b0025120b07`
WHERE contact=1
AND datetime>'2022-11-01'
GROUP BY left(datetime,10);

-- Дверь холодильника
SELECT left(datetime,10),count(*) from `0x00124b0025130e7d`
WHERE contact=1
AND datetime>'2022-11-03'
GROUP BY left(datetime,10);

EXPLAIN
SELECT * FROM `0x00124b0025130e7d`
ORDER BY `datetime` DESC
LIMIT 1;

UPDATE dashboard SET datetime=CURRENT_TIMESTAMP, json_data = '{}'
WHERE alias = 'pult1'

