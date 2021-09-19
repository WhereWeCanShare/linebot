# LINE Bot

## webhook
- `/l2tg` - line2telegram: forward text message from LINE group/room to Telegram chat

## .env file 
require to define system variables ie. Token, API key, Password

## need
- LINE messaging API account and token, get from https://developers.line.biz/console
- Web hosting to host this Python code, with the HTTPS (443).

## suggest
- run the Python code using the Unix sock instead of HTTP.
- on the web serivce e.g. nginx, do the reverse proxy to sock `proxy_pass http://unix:/apps/linebot/linebot.sock;`

