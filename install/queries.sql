SELECT left(datetime,10),count(*) from `0x00124b0025120b07`
WHERE contact=1
AND datetime>'2022-10-17'
GROUP BY left(datetime,10);
