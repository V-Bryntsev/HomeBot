# HomeBot
Telegram bot for home

Build Dockerfile:
```
docker build --tag telegram_bot .
```
*For work ipmi on my server i need mapping /dev/ipmi0 device to container. So i use ubuntu image (not just python).\
Run container:
```
docker run -ti --name telegram_bot --device /dev/ipmi0 telegram_bot
```

Commands for bot:\
\parking - show screenshot from camera on balcony, which look to parking (get jpeg from camera and send to chat)\
\getsrvtemp - show temperature from home server sensors (use local ipmitool command on server)\
\transponder - show balance of my avtodor transponder (authorization on site and parsing html)\
