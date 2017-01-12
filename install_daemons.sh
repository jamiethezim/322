#clone postgres repo
git clone -b REL9_5_STABLE https://github.com/postgres/postgres.git
cd postgres
./configure --prefix=$1
make
make install
curl http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2
cd httpd-2.4.25
./configure --prefix=$1
make
make install
