create_tables.sql -> just a long list of CREATE TABLE statements. Followed the lost_req.pdf for information on the data model. Each table has a primary key, not of data type int but of serial primary key.

gen_insert2.py -> take 2 on the previous python script to import all the legacy data. Uses psychopg2 to connect to the database and port, which are user specified arguments. has functions for insert into the assets, asset_at, and facilities table. The most important columns were asset tag and fcode, because that's all the next assignment really cares about.

import_data.sh -> curls the legacy files locally and unzips them. runs the create_tables sql script, and executes gen_insert2 python script to parse and import all the unzipped legacy data. 
