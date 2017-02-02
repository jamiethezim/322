CREATE TABLE products(
	product_pk serial primary key,
	vendor text,
	description text,
	alt_description text
);
CREATE TABLE assets(
	asset_pk serial primary key,
	product_fk int,
	asset_tag text,
	description text,
	alt_description text
);

CREATE TABLE vehicles(
	vehicle_pk serial primary key,
	asset_fk int
);

CREATE TABLE facilities(
	facility_pk serial primary key,
	fcode text,
	common_name text,
	location text
);

CREATE TABLE asset_at(
	asset_fk serial primary key,
	facility_fk int,
	arrive_dt timestamp,
	depart_dt timestamp
);

CREATE TABLE convoys(
	convoy_pk serial primary key,
	request text,
	source_fk int,
	dest_fk int,
	depart_dt timestamp,
	arrive_dt timestamp
);

CREATE TABLE used_by(
	vehicle_fk serial primary key,
	convoy_fk int
);

CREATE TABLE asset_on(
	asset_fk serial primary key,
	convoy_fk int,
	load_dt timestamp,
	unload_dt timestamp
);

CREATE TABLE users(
	user_pk serial primary key,
	username text,
	active boolean
);

CREATE TABLE roles(
	role_pk serial primary key,
	title text
);

CREATE TABLE user_is(
	user_fk serial primary key,
	role_fk int
);

CREATE TABLE user_supports(
	user_fk serial primary key,
	facility_fk int
);

CREATE TABLE levels(
	level_pk serial primary key,
	abbrv text,
	comment_ text
);

CREATE TABLE compartments(
	compartment_pk serial primary key,
	abbrv text,
	comment_ text
);

CREATE TABLE security_tags(
	tag_pk serial primary key,
	level_fk int,
	compartment_fk int,
	user_fk int,
	product_fk int,
	asset_fk int
);
