sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE stepik_web;"
mysql -uroot -e "CREATE USER 'box@localhost' IDENTIFIED BY 'stepik';"
mysql -uroot -e "GRANT ALL ON stepik_web.* TO 'box@localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"
