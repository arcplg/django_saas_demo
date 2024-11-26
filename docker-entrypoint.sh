#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until mysql -h "$host" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "select 1;" &>/dev/null; do
  echo "Waiting for MySQL..."
  sleep 1
done

exec $cmd
