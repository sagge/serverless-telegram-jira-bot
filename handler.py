import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./modules"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


def listen_and_send(event, context):
    try:
        data = json.loads(event["body"])
        # print(data)
        message = ""
        event = str(data["webhookEvent"])
        issue = str(data["issue"]["key"])
        issue_summary = str(data["issue"]["fields"]["summary"])
        url = "https://aatos.atlassian.net/browse/" + issue
        user = str(data["user"]["displayName"])

        if event == "jira:issue_deleted":
            message = 'Issue: "' + issue_summary + '" deleted by ' + user
        elif event == "jira:issue_created":
            message = 'Issue: "' + issue_summary + '" created by ' + user + '. ' + url + '. '
        else:
            message = event.replace("jira:", "").replace("_", " ").capitalize() + ' by ' + user + '. ' + url + '. ' + "Changelog: " + str(data["changelog"]["items"])

        data = {"text": message.encode("utf8"), "chat_id": CHAT_ID}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}