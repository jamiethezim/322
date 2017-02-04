CREATE TABLE logins (
	-- usernames and passwords have 1-1 relationship
	-- i want to keep in one table
	-- honestly probably don't need numeric tabling for users...
	-- but in case I build later tables for things that users own
	-- I might end up needing user_fk, in which it is helpful
	user_pk serial primary key,
	username varchar(16), --usernames are <= 16 chars
	password varchar (16) --passwords are <= 16 chars
);
