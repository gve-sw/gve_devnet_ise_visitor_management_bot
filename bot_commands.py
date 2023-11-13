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

from dotenv import load_dotenv
from ise import ISE
from utils import Utils
from datetime import datetime
from webexteamssdk import WebexTeamsAPI

load_dotenv()

class BotCommands():

    def __init__(self, token, lobby_user):
        self.token = token 
        self.ise = ISE()
        self.lobby_user = lobby_user
        self.api = WebexTeamsAPI(access_token=token)


    '''
    Method to return the personal or all (depending on privileges) guest users via Webex card. 
    '''
    def get_guest_users(self, incoming_msg):

        room_id = incoming_msg.roomId

        try:
            card_content = Utils.read_json('webex_card_templates/visitor_list.json')
            email = incoming_msg.personEmail
            facts = []
            users_details = []

            if Utils.is_visitor_management_admin(self.lobby_user, email) != None:
                filter=""
            else:
                filter = f"?filter=personBeingVisited.EQ.{email}"
            
            users = self.ise.get_guest_users(filter=filter)

            for user in users['SearchResult']['resources']:
                ise_user_id = user['id']
                user_details = self.ise.get_guest_user_by_ID(ise_user_id)
                users_details.append(user_details['GuestUser'])

            for user in users_details:
                guest_name = f"{user['guestInfo'].get('firstName', '')} {user['guestInfo'].get('lastName', '')}"
                guest_company = f"{user['guestInfo'].get('company', '-')}"
                date_range = f"{user['guestAccessInfo'].get('fromDate','')} - {user['guestAccessInfo'].get('toDate','')}"

                facts.append({
                    "title": f"{date_range}",
                    "value": f"{guest_name} ({guest_company})"
                    })
                        
            card_content['body'][2]['facts'] = facts

            self.send_webex_room_card(room_id, card_content)
        
        except Exception as e:

            error_card_content = self.get_error_card_content(e)
            self.send_webex_room_card(room_id, error_card_content)
            pass
 
        return ""


    '''
    Method returning a form card for guest user creation.
    '''
    def create_guest_user(self,incoming_msg):
        
        card_content = Utils.read_json('webex_card_templates/visitor_form.json')
        room_id = incoming_msg.roomId

        self.send_webex_room_card(room_id, card_content)

        return ""


    '''
    Method reading user input, creating guest user and notifiying user and guest. 
    '''
    # check attachmentActions:created webhook to handle the submit card actions 
    def handle_cards(self, api, incoming_msg):

        try:
            m = self.api.attachment_actions.get(incoming_msg['data']['id'])
            person = self.api.people.get(incoming_msg['data']['personId'])
            message_data = m.inputs

            building = message_data['building']           
            phone_number = message_data['phone']  
            company = message_data['company']  
            comment = message_data['comment']  
            email = message_data['email']  
            purpose = message_data['purpose']  
            badge_id = message_data['badge_id'] 
            check_in = message_data['check_in']   
            host_email = person.emails[0]
            host_name = f"{person.firstName} {person.lastName}"
            firstname = message_data['first_name']  
            lastname = message_data['last_name']  
            now_date_string = datetime.now().strftime("%m%d%Y_%H%M%S")
            username = f"{firstname}_{lastname}_{now_date_string}".replace(" ", "")
            start_date = f"{message_data['start_date']}T{message_data['start_time']}"
            end_date = f"{message_data['end_date']}T{message_data['end_time']}" 
            visit_date = start_date + "-" + end_date

            #TODO fix error here
            
            self.ise.create_guest_user(username, comment, firstname, lastname, email, phone_number, company, start_date, end_date, check_in, host_email, building, purpose, host_name, badge_id)
            
            user_response_success_card = Utils.read_json('webex_card_templates/user_response.json')
            self.send_webex_room_card(m.roomId, user_response_success_card)

            if email != "":
                
                created_user = self.ise.get_guest_based_on_username(username)
                username = created_user['GuestUser']['guestInfo']['userName']
                password = created_user['GuestUser']['guestInfo']['password']
                ssid = created_user['GuestUser']['guestAccessInfo']['ssid']

                self.send_visitor_notifications(email, host_name, building, visit_date, ssid, username, password)
            
        except Exception as e:
            error_card_content = self.get_error_card_content(e)
            self.send_webex_room_card(m.roomId, error_card_content)
            pass

        return ""


    '''
    Method to send webex card to invited guest user.
    '''
    def send_visitor_notifications(self, visitor_email, host_name, building, date, ssid, username, password):
        
        print(f"Send Webex message to visitor. {visitor_email}")
        visitor_card_content = self.prepare_visitor_notification_card(host_name, building, date, ssid, username, password)
        self.send_webex_direct_message_card(visitor_email, visitor_card_content)


    '''
    Method to populate the Webex card template with specific guest user information.
    '''
    def prepare_visitor_notification_card(self, host_name, building, date, ssid, username, password):

        visitor_card = Utils.read_json('webex_card_templates/visitor_response.json')
        visitor_card['body'][1]['columns'][1]['items'][0]['text'] = host_name
        visitor_card['body'][2]['columns'][1]['items'][0]['text'] = building
        visitor_card['body'][3]['columns'][1]['items'][0]['text'] = date
        visitor_card['body'][5]['columns'][1]['items'][0]['text'] = ssid
        visitor_card['body'][6]['columns'][1]['items'][0]['text'] = username
        visitor_card['body'][7]['columns'][1]['items'][0]['text'] = password

        return visitor_card


    '''
    Method to send card as direct Webex message.
    '''
    def send_webex_direct_message_card(self, toPersonEmail, card_content):

        self.api.messages.create(toPersonEmail=toPersonEmail, text="If you see this your client cannot render cards.", attachments=[{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_content
            }])


    '''
    Method to send card as to Webex room.
    '''
    def send_webex_room_card(self, room_id, card_content):

        self.api.messages.create(text="If you see this your client cannot render cards.", roomId=room_id, attachments=[{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_content
            }])

    
    '''
    Method to populate error card based on the occured error.
    '''
    def get_error_card_content(self, e):
        print(f"An error happened: {e}")
        user_response_error = Utils.read_json('webex_card_templates/user_response_error.json')
        user_response_error['body'][1]['text'] = f"An error happened: {e}"
        return user_response_error 


    