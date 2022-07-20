ARG MONGO_TAG=${MONGO_TAG}
FROM mongo:${MONGO_TAG}

VOLUME /data/db /data/configdb

COPY docker-entrypoint/* /docker-entrypoint-initdb.d/

CMD ["mongod"]

EXPOSE 27017
