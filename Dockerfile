FROM ubuntu:latest
WORKDIR /app
COPY . .

ADD crontab /etc/cron.d/azure-trigger-sync
RUN chmod 0644 /etc/cron.d/azure-trigger-sync

RUN touch /var/log/cron.log

# install necessary packages
RUN apt-get update
RUN apt-get -y install cron python3.9 python3-pip
RUN pip install -r /app/requirements.txt

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
