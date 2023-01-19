-- Статистика по открыванию двери (туалета)
SELECT left(datetime,10) AS `DATE`, count(*) AS `COUNT` from `0x00124b0025120b07`
WHERE contact=1
AND datetime>DATE_SUB(NOW(), INTERVAL 20 DAY)
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
WHERE alias = 'pult1';

-- Записи, идущие чаще, чем раз в 60 секунд
SELECT a.id, a.datetime, b.id, b.datetime, b.temperature FROM `0xa4c138c934616c86` a
JOIN `0xa4c138c934616c86` b ON a.id = b.id + 1 AND TIMESTAMPDIFF(SECOND, b.datetime, a.datetime) < 60
LIMIT 20;

-- Удаляем слишком часто идущие записи (оставляем не чаще, чем раз в минуту60 секунд)
DELETE FROM `0xa4c138eb4d0d071f` WHERE id in (SELECT b.id
                                              FROM `0xa4c138eb4d0d071f` a
                                                       JOIN `0xa4c138eb4d0d071f` b
                                                            ON a.id = b.id + 1 AND TIMESTAMPDIFF(SECOND, b.datetime, a.datetime) < 60

                                              );


-- LIMIT 20000;
-- Обновляем поле перед удалением лишних записей
UPDATE sensor SET received_events = (SELECT COUNT(1) from `0xa4c138b3e4db875f`)
WHERE device_id = '0xa4c138b3e4db875f'