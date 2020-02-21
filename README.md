# Serverless telegram bot to catch Jira Cloud webhooks

```
pip3 install -r requirements.txt -t modules
```

```
export TELEGRAM_TOKEN="<TELEGRAM_TOKEN>"
export CHAT_ID="<CHAT_ID>"
```

```
sls deploy
```

Configure Jira Webhooks to point to your lambda