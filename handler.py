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
        print(data)
        message = ""
        event = str(data["webhookEvent"])
        issue = str(data["issue"]["key"])
        issue_summary = str(data["issue"]["fields"]["summary"])
        url = "https://aatos.atlassian.net/browse/" + issue

        if event == "jira:issue_deleted":
            user = str(data["user"]["displayName"])
            message = '🚮 Issue: "{}" deleted by {}.'.format(issue_summary, user)
        elif event == "jira:issue_created":
            user = str(data["user"]["displayName"])
            message = '🐣 Issue: "{}" created by {}. {}'.format(issue_summary, user, url)
        elif event == "jira:issue_updated":
            user = str(data["user"]["displayName"])
            changelog = data["changelog"]["items"][0]
            if changelog["field"] == "description":
                description = str(changelog["toString"])
                message = '{} updated the decrption of "{}" to "{}"'.format(user, issue_summary, description)
            elif changelog["field"] == "summary":
                from_string = str(changelog["fromString"])
                to_string = str(changelog["toString"])
                message = '{} updated issue "{}" to "{}"'.format(user, from_string, to_string)
            elif changelog["field"] == "status":
                from_string = str(changelog["fromString"])
                to_string = str(changelog["toString"])
                message = '{} updated issue "{}" status from "{}" to "{}"'.format(user, issue_summary, from_string, to_string)
            elif changelog["field"] == "labels":
                from_string = str(changelog["fromString"])
                to_string = str(changelog["toString"])
                message = '{} updated issue "{}" labels from "{}" to "{}"'.format(user, issue_summary, from_string, to_string)
            elif changelog["field"] == "assignee":
                to_string = str(changelog["toString"])
                message = '"{}" assigned to {}'.format(issue_summary, to_string)
            else:
                message = 'Issue "{}" updated by {}. Changelog: {}.'.format(issue_summary, user, str(data["changelog"]["items"]))
        elif event == "comment_created":
            user = str(data["comment"]["author"]["displayName"])
            comment = str(data["comment"]["body"])
            message = '💬 {} commented on issue "{}": "{}"'.format(user, issue_summary, comment)
        elif event == "comment_updated":
            user = str(data["comment"]["updateAuthor"]["displayName"])
            comment = str(data["comment"]["body"])
            message = '💬 {} updated comment on issue "{}": "{}"'.format(user, issue_summary, comment)
        elif event == "comment_deleted":
            user = str(data["comment"]["updateAuthor"]["displayName"])
            comment = str(data["comment"]["body"])
            message = '💬 {} deleted comment on issue "{}": "{}"'.format(user, issue_summary, comment)
        else:
            raise ValueError('Event type not recognized')

        data = {"text": message.encode("utf8"), "chat_id": CHAT_ID}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}