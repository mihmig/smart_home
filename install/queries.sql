-- Статистика по открыванию двери (туалета)
SELECT left(datetime,10) AS `DATE`, count(*) AS `COUNT` from `0x00124b0025120b07`
WHERE contact=1
AND datetime>DATE_SUB(NOW(), INTERVAL 10 DAY)
GROUP BY left(datetime,10);

-- Статистика по открыванию двери (холодильника)
SELECT left(datetime,10) AS `DATE`, count(*) AS `COUNT` from `0x00124b0025130e7d`
WHERE contact=1
AND datetime>DATE_SUB(NOW(), INTERVAL 10 DAY)
GROUP BY left(datetime,10);

-- Статистика по открыванию двери в квартиру
SELECT left(datetime,10) AS `DATE`, count(*) AS `COUNT` from `0x00124b002511e75e`
WHERE contact=1
AND datetime>DATE_SUB(NOW(), INTERVAL 10 DAY)
GROUP BY left(datetime,10);

EXPLAIN
SELECT * FROM `0x00124b0025130e7d`
ORDER BY `datetime` DESC
LIMIT 1;

UPDATE dashboard SET datetime=CURRENT_TIMESTAMP, json_data = '{}'
WHERE alias = 'pult1'

