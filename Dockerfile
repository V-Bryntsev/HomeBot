FROM ubuntu:16.04
COPY . /app
WORKDIR /app
RUN apt update && apt install -y ipmitool python3 python3-pip iputils-ping && pip3 install -r requirements.txt
ENTRYPOINT python3 ./telegram_bot.py