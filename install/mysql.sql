CREATE TABLE `sensor`
(
	id INT AUTO_INCREMENT,
	unique_id VARCHAR(255) NOT NULL,
	device_model VARCHAR(255) NOT NULL,
	device_type INT NULL,
	`description` VARCHAR(255) NULL,
	alias VARCHAR(255) NULL,
	received_events INT NULL DEFAULT 0 COMMENT 'Количество событий, поступивших от датчика',
	CONSTRAINT device PRIMARY KEY (id)
) ENGINE=InnoDB;
CREATE UNIQUE INDEX sensor__unique_id ON sensor (unique_id);

# DROP TABLE `dashboard`;

CREATE TABLE `dashboard`
(
	id INT AUTO_INCREMENT,
	`datetime` TIMESTAMP,
	`alias` VARCHAR(255) NOT NULL,
	`json_data` JSON NULL,
	CONSTRAINT device PRIMARY KEY (id),
	UNIQUE KEY (`alias`)
) ENGINE=InnoDB;
ALTER TABLE `dashboard` COMMENT='Показания и состояния датчиков для панели мониторинга';

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
ALTER TABLE `0x00124b002511e75e` COMMENT='SONOFF SNZB-04';
CREATE OR REPLACE INDEX `0x00124b002511e75e_datetime_idx` ON `0x00124b002511e75e`(`datetime` DESC);

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
ALTER TABLE zigbee.`0x00124b0025120b07` COMMENT='SONOFF SNZB-04';
CREATE OR REPLACE INDEX `0x00124b0025120b07_datetime_idx` ON `0x00124b0025120b07`(`datetime` DESC);

-- Датчик открытия
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
ALTER TABLE `0x00124b0025130e7d` COMMENT='SONOFF SNZB-04';
CREATE OR REPLACE INDEX `0x00124b0025130e7d_datetime_idx` ON `0x00124b0025130e7d`(`datetime` DESC);

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
ALTER TABLE `0xa4c138c934616c86` COMMENT='TuYa WSD500A Температура и влажность T1';
CREATE OR REPLACE INDEX `0xa4c138c934616c86_datetime_idx` ON `0xa4c138c934616c86`(`datetime` DESC);

-- Датчик температуры и влажности (TuYa WSD500A)
CREATE TABLE `0xa4c138187be8cae9`
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
ALTER TABLE `0xa4c138187be8cae9` COMMENT='TuYa WSD500A Температура и влажность T4';
CREATE OR REPLACE INDEX `0xa4c138187be8cae9_datetime_idx` ON `0xa4c138187be8cae9`(`datetime` DESC);

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
ALTER TABLE `0xa4c138110e938e98` COMMENT='TuYa CX-7026 Температура и влажность';
CREATE OR REPLACE INDEX `0xa4c138110e938e98_datetime_idx` ON `0xa4c138110e938e98`(`datetime` DESC);

-- Датчик освещённости, температуры и влажности (ZSS-ZK-THL)
CREATE TABLE `0x847127fffefc9500`
(
    id INT AUTO_INCREMENT,
    `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    illuminance_lux INT,
    battery FLOAT,
    linkquality INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE `0x847127fffefc9500` COMMENT='Датчик освещённости, температуры и влажности (ZSS-ZK-THL)';
CREATE OR REPLACE INDEX `0x847127fffefc9500_datetime_idx` ON `0x847127fffefc9500`(`datetime` DESC);

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
ALTER TABLE `0xa4c138f7f972b7b0` COMMENT='WHD02 Реле 220В';
CREATE OR REPLACE INDEX `0xa4c138f7f972b7b0_datetime_idx` ON `0xa4c138f7f972b7b0`(`datetime` DESC);

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
ALTER TABLE `0xa4c1383b6db1be29` COMMENT='WHD02 Реле 220В';
CREATE OR REPLACE INDEX `0xa4c1383b6db1be29_datetime_idx` ON `0xa4c1383b6db1be29`(`datetime` DESC);

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
ALTER TABLE `0xa4c138ffef6b9d70` COMMENT='SS6400ZB-V2 4-х кнопочный пульт';
CREATE OR REPLACE INDEX `0xa4c138ffef6b9d70_datetime_idx` ON `0xa4c138ffef6b9d70`(`datetime` DESC);


GRANT ALL PRIVILEGES ON zigbee.* TO 'zigbee'@'%';
FLUSH PRIVILEGES;
