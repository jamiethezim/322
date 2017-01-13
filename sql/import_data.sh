#curl the legacy files
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy.tar.gz
#unzip the compressed data
tar -xvzf legacy.tar.gz

#run python scripts
python3 gen_insert.py > insert.sql
#run insert scripts
psql $1 -f insert.sql
#clean up
rm insert.sql
