create table `device`
(
	id int auto_increment,
	unique_id varchar(255) not null,
	device_model varchar(255) not null,
	device_type int null,
	description varchar(255) null,
	constraint device
		primary key (id)
) ENGINE=MyISAM;

create unique index device__unique_id
	on device (unique_id);
#
# create table `open_close`
# (
# 	id int auto_increment,
# 	device_id int not null,
# 	datetime timestamp not null,
# 	state int not null,
# 	constraint open_close_pk
# 		primary key (id)
# ) ENGINE=MyISAM;
#
# create index open_close_device_id_uindex
# 	on open_close (device_id);

-- Датчик открытия
CREATE TABLE `0x00124b002511e75e`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    battery FLOAT,
    battery_low BOOL,
    contact BOOL,
    linkquality INT,
    tamper BOOL,
    voltage INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0x00124b002511e75e` COMMENT='SONOFF SNZB-04 Входная дверь';

-- Датчик открытия
CREATE TABLE `0x00124b0025120b07`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    battery FLOAT,
    battery_low BOOL,
    contact BOOL,
    linkquality INT,
    tamper BOOL,
    voltage INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0x00124b0025120b07` COMMENT='SONOFF SNZB-04 Дверь туалета';

-- Датчик открытия (Дверь холодильника)
CREATE TABLE `0x00124b0025130e7d`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    battery FLOAT,
    battery_low BOOL,
    contact BOOL,
    linkquality INT,
    tamper BOOL,
    voltage INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0x00124b0025130e7d` COMMENT='SONOFF SNZB-04 Дверь холодильника';

-- Датчик температуры и влажности (TuYa WSD500A)
CREATE TABLE `0xa4c138c934616c86`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    battery FLOAT,
    linkquality INT,
    voltage INT,
    temperature FLOAT,
    humidity FLOAT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0xa4c138c934616c86` COMMENT='TuYa WSD500A Температура и влажность в спальне';

-- Датчик температуры и влажности LCD (TuYa CX-7026)
CREATE TABLE `0xa4c138110e938e98`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    battery FLOAT,
    linkquality INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0xa4c138110e938e98` COMMENT='TuYa WSD500A Температура и влажность';

-- Реле 220В
CREATE TABLE `0xa4c138f7f972b7b0`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    linkquality INT,
    power_on_behavior VARCHAR(20),
    state VARCHAR(20),
    switch_type VARCHAR(20),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0xa4c138f7f972b7b0` COMMENT='WHD02 Реле 220В';

-- Реле 220В
CREATE TABLE `0xa4c1383b6db1be29`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    linkquality INT,
    power_on_behavior VARCHAR(20),
    state VARCHAR(20),
    switch_type VARCHAR(20),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0xa4c1383b6db1be29` COMMENT='WHD02 Реле 220В';

-- SS6400ZB-V2 4-х кнопочный пульт
CREATE TABLE `0xa4c138ffef6b9d70`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    battery INT,
    linkquality INT,
    action VARCHAR(20),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE zigbee.`0xa4c138ffef6b9d70` COMMENT='SS6400ZB-V2 4-х кнопочный пульт';



GRANT ALL PRIVILEGES ON zigbee.* TO 'zigbee'@'%';
FLUSH PRIVILEGES;
