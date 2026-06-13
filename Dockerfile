FROM postgres:16
RUN apt-get update && apt-get install -y postgresql-16-cron
COPY postgresql.conf /etc/postgresql/postgresql.conf
# CMD sorgt dafür, dass die Config geladen wird
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]