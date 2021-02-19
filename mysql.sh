sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE stepik-web;"
mysql -uroot -e "CREATE USER 'django@localhost' IDENTIFIED BY 'stepik';"
mysql -uroot -e "GRANT ALL ON stepik_web.* TO 'django@localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"
