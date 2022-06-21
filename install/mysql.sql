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

create table `open_close`
(
	id int auto_increment,
	device_id int not null,
	datetime timestamp not null,
	state int not null,
	constraint open_close_pk
		primary key (id)
) ENGINE=MyISAM;

create index open_close_device_id_uindex
	on open_close (device_id);
