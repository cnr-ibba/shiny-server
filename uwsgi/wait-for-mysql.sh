#!/bin/bash
# wait-for-mysql.sh
# https://docs.docker.com/compose/startup-order/
# adapted from https://raw.githubusercontent.com/agileek/docker/master/tomcat/wait-for-mysql.sh

set -e
set -x

cmd="$@"

NEXT_WAIT_TIME=0
MAX_STEPS=6

until mysql -h db -u ${SHINY_USER} -p${SHINY_PASSWORD} ${SHINY_DATABASE} -e 'select 1' || [ ${NEXT_WAIT_TIME} -eq ${MAX_STEPS} ]; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 5
  NEXT_WAIT_TIME=$((NEXT_WAIT_TIME+1))
done

if [ ${NEXT_WAIT_TIME} -eq ${MAX_STEPS} ]; then
  >&2 echo "Problem in waiting MySQL"
  exit 1;
fi

>&2 echo "MySQL is up - executing command"
exec $cmd
