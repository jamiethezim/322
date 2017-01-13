#curl the legacy files
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy.tar.gz
tar -xvzf legacy.tar.gz
cd osnap_legacy
#run python scripts
##python3 gen_insert.py > insert.sql
#run insert scripts
##psql lost_db -f insert.sql
#clean up
##rm insert.sql
