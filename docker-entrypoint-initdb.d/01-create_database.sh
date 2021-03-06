#!/bin/bash
set -e

mysql --user=root --password=${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE ${SHINY_DATABASE} DEFAULT CHARACTER SET 'utf8' DEFAULT COLLATE 'utf8_bin'"
mysql --user=root --password=${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${SHINY_DATABASE}.* to '${SHINY_USER}'@'%' IDENTIFIED BY '${SHINY_PASSWORD}'"
mysql --user=root --password=${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${SHINY_DATABASE}.* to '${SHINY_USER}'@'localhost' IDENTIFIED BY '${SHINY_PASSWORD}'"

# test instance for django
mysql --user=root --password=${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON test_${SHINY_DATABASE}.* to '${SHINY_USER}'@'%' IDENTIFIED BY '${SHINY_PASSWORD}'"
mysql --user=root --password=${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON test_${SHINY_DATABASE}.* to '${SHINY_USER}'@'localhost' IDENTIFIED BY '${SHINY_PASSWORD}'"
