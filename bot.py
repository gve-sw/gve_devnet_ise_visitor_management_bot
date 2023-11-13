""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

import os
from dotenv import load_dotenv
from webexteamsbot import TeamsBot
from bot_commands import BotCommands

load_dotenv()

bot_email = os.getenv('WEBEX_BOT_EMAIL')
teams_token = os.getenv('WEBEX_BOT_TOKEN')
bot_url = os.getenv('WEBEX_BOT_URL')
bot_app_name = os.getenv('WEBEX_BOT_APP_NAME')
lobby_user = os.environ['LOBBY_USERS'].split(",")
base_users = os.environ['BASE_USERS'].split(",")

approved_users = list(lobby_user) + list(base_users)


'''
Create the bot
'''
bot = TeamsBot(
    bot_app_name,
    WEBEX_BOT_TOKEN=teams_token,
    WEBEX_BOT_URL=bot_url,
    WEBEX_BOT_EMAIL=bot_email,
    webhook_resource_event=[{"resource": "messages", "event": "created"},
                            {"resource": "attachmentActions", "event": "created"}],
    approved_users=approved_users
)


'''
Create the bot commands
'''
bot_commands = BotCommands(teams_token, lobby_user) 

bot.set_help_message("I support the following commands:\n")
bot.add_command("/create", "Trigger process to create a new ISE guest user", bot_commands.create_guest_user)
bot.add_command("/show", "Show own or all guest users based on privileges", bot_commands.get_guest_users)
bot.add_command('attachmentActions', '*', bot_commands.handle_cards)

bot.remove_command("/echo")


if __name__ == "__main__":
    bot.run(host="0.0.0.0", port=5001)