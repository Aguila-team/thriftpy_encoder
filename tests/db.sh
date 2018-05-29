#!/usr/bin/env bash
set +x

if [ $# -eq 0 ]; then
    echo "Err: username required. Usage: './db.sh username'"
else
    echo "Start executing SQL commands"
    mysql -u$1 -p -e "source database/schema.sql"
fi