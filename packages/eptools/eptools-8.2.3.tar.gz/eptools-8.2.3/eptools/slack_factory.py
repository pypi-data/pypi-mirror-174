import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from eptools.configuration import *

    
# Utils
# ---

def reloadconfig(func):  
    def wrap(*args, **kwargs):
        setglobals(globals())
        getglobals_new_globals = getglobals()
        globals().update(getglobals_new_globals)
        func_new_globals = func(*args,**kwargs)
        after_func_new_globals = getglobals()
        globals().update(after_func_new_globals)
        return func_new_globals
    return wrap

loadconfigwithfile = reloadconfig(loadconfigwithfile)
loadconfigwithjson = reloadconfig(loadconfigwithjson)


# Slack Factory
# ---
# This Python module can be used to send Slack notifications
# 
# Slack Docs:           https://slack.dev/python-slack-sdk/
# Block Kit Builder:    https://app.slack.com/block-kit-builder/
# 
# Test channel ID: C0489AUFV8V
# Test channel Name: testing

class SlackFactory:
    @reloadconfig
    def __init__(self, config_path=None) -> None:
        loadconfigwithfile(config_path)
        self.logger = logging.getLogger(__name__)
        self.client = WebClient(token=globals()['C_SLACK_TOKEN'])
    
    def send_message(self, channel_id, message) -> dict:
        try:
            response = self.client.chat_postMessage(
                channel = channel_id,
                text = message
            )
            return response
        except SlackApiError as e:
            assert e.response["error"]
            
    def send_formatted_message(self, channel_id, blocks, short_description=None) -> dict:
        if not short_description:
            short_description = "EasyBot has something to tell you!"

        try:
            
            print(channel_id)
            print(blocks)
            print(short_description)
            
            response = self.client.chat_postMessage(
                channel = channel_id,
                text = short_description,
                blocks = blocks
            )
            self.logger.info(response)
            return response
        except SlackApiError as e:
            assert e.response["error"]
            
    def get_all_channels(self) -> list:
        try:
            response = self.client.conversations_list()
            return response['channels']
        except SlackApiError as e:
            assert e.response["error"]
            
    def get_channel_info(self, channel_id) -> dict:
        try:
            response = self.client.conversations_info(channel=channel_id)
            return response['channel']
        except SlackApiError as e:
            assert e.response["error"]

# Testing 
# ---
            
if __name__ == '__main__':
    slack_factory = SlackFactory()
        
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "New request :ghost:"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Type:*\nPaid Time Off"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Created by:*\n<example.com|Fred Enriquez>"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*When:*\nAug 10 - Aug 13"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<https://example.com|View request>"
            }
        }
    ]
    
    res = slack_factory.send_formatted_message('C0489AUFV8V', blocks, '*beep boop*')
    print(res)