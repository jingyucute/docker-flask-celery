#!/bin/bash
set -e

if [[ -n ${MONGO_INITDB_USERNAME} && -n ${MONGO_INITDB_PASSWORD} ]];
then 
    echo "Add User ${MONGO_INITDB_USERNAME} To ${MONGO_INITDB_DATABASE}";
else 
    echo "Not Create user";
    exit;
fi

mongo admin -u $MONGO_INITDB_ROOT_USERNAME  -p $MONGO_INITDB_ROOT_PASSWORD <<EOF
use ${MONGO_INITDB_DATABASE};
db.init.insert({init:1});
db.createUser({
    user:  "${MONGO_INITDB_USERNAME}",
    pwd: "${MONGO_INITDB_PASSWORD}",
    roles: ["dbOwner"]
});
EOF