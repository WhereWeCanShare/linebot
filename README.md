# LINE Bot

## webhook

- `/l2tg` - line2telegram: forward text message from LINE group/room to Telegram chat

## Requirement

- LINE Message API read more about LINE Message API and Channel at https://developers.line.biz/en/docs/messaging-api/overview/
- Telegram Bot how to create a bot read this https://core.telegram.org/bots
- Web hosting with HTTPS support

## .env file 

require to define system variables ie. Token, API key,

```
LINE_TOKEN=
TG_TOKEN=
TG_CHANNEL=
```

## host at Heroku

- create an apps on Heroku
- define all variables if you do not use .env file.
- upload code to Heroku.
