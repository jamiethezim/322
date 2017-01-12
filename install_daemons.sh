#clone postgres repo
git clone https://github.com/postgres/postgres.git
cd postgres
./configure
make
make install
curl http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2
cd httpd-2.4.25
./configure --prefix=$HOME/installed
make
make install
