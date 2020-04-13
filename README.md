# HomeBot
Telegram bot for home

Build Dockerfile:
```
docker build --tag telegram_bot .
```
*For work ipmi on my server i need mapping /dev/ipmi0 device to container. So i use ubuntu image (not just python).
Run container:
```
docker run -ti --name python-app --device /dev/ipmi0 telegram_bot
```
