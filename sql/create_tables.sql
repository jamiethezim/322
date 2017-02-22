CREATE TABLE roles (
	role_pk serial primary key,
	role varchar(20)
);
CREATE TABLE logins (
	-- usernames and passwords have 1-1 relationship
	-- i want to keep in one table
	-- honestly probably don't need numeric tabling for users...
	-- but in case I build later tables for things that users own
	-- I might end up needing user_fk, in which it is helpful
	user_pk serial primary key,
	username varchar(16), --usernames are <= 16 chars
	password varchar (16), --passwords are <= 16 chars
	role_fk integer REFERENCES roles(role_pk) --users can only have one role, but could have potentially one of many different kinds of roles, so I created another table of roles
);

CREATE TABLE assets (
	asset_pk serial primary key,
	asset_tag varchar(32),
	description text,
	disposed boolean
);

CREATE TABLE facilities (
	facility_pk serial primary key,
	fcode varchar(16),
	common_name varchar(128)
);

CREATE TABLE asset_at (
	asset_fk integer REFERENCES assets(asset_pk),
	facility_fk integer REFERENCES facilities(facility_pk),
	arrive_dt timestamp,
	depart_dt timestamp
);
-- asset_at table maps assets table to facilities table
-- with asset_fk and facility_fk
