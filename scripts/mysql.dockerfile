FROM mysql:8
ENV MYSQL_ROOT_PASSWORD asdf
ENV MYSQL_USER swapiuser
ENV MYSQL_PASSWORD asdf
ENV MYSQL_DATABASE swapi
ADD 10-tables.sql /docker-entrypoint-initdb.d
EXPOSE 3306
