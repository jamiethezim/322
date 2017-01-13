#curl the legacy files
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy.tar.gz
#unzip the compressed data
tar -xvzf legacy.tar.gz


psql $1 -f create_tables.sql
#run python scripts
python3 gen_insert2.py $1 $2
