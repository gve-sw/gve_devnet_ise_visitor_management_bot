# gve_devnet_ise_visitor_management_bot

This demo shows a visitor management bot based on the ISE guest user feature. Thereby, the bot automatically adapts to the privilege level of the requesting account. 
The bot allows the creation and viewing of personal visitors for base users. Lobby users can create new visitors and view all visitors available. 
Invited visitors are informed about the invitation and associated access information via Webex. The user is informed about the successful completion of the process. 

This demo can be used as an addition to the repository https://github.com/gve-sw/gve_devnet_ise_visitor_management.


## Contacts
* Ramona Renner


## Solution Components
* Cisco ISE
* Webex


## Workflow

![/IMAGES/0image.png](/IMAGES/workflow.png)

## Architecture

![/IMAGES/0image.png](/IMAGES/arch.png)

## Prerequisites

### Create a Webex Bot

1. Log in to **developer.webex.com**
2. Click on your avatar and select `My Webex Apps`
3. Click `Create a New App`
4. Click `Create a Bot` to start the wizard
5. Following the instructions of the wizard, provide your `bot's name, username, and icon`
6. Once the form is filled out, click `Add Bot` and you will be given an `access token`
7. Copy the access token and store it safely. Please note that the API key will be shown only once for security purposes. If you lose the key, you have to revoke it and generate a new one.

### Webhooks

The app needs to be reachable on port 5001 from the public internet for Webex Webhooks to be received and processed. Any option is valid, like AWS Lambda, Heroku, GCP, etc. Ngrok is used here to expose the local app for simplicity.

#### Ngrok

The Flask app runs on http://localhost:5001 by default, so it requires a Ngrok forwarding address to port 5001 to receive the webhooks.

Follow these instructions to set up ngrok:

1. Create a free account or login to [Ngrok](https://ngrok.com/).
2. Retrieve your auth token by navigating to `Getting Started > Your Authtoken` on the menu on the left-hand side. Copy the token on this page.
3. Then install the client library, depending on your OS [here](https://ngrok.com/download).
4. Once you have ngrok installed, update the ngrok configuration file with your auth token by running the following command on the terminal/command prompt:   

    ```ngrok authtoken <yourtoken>```   

replacing <yourtoken> with the authtoken you copied in Step 2.   

5. Start the ngrok tunnel for port 5001 with the command:

    ```ngrok http 5001```   

Note the link under `Forwarding` with the format `http://xxxxx.ngrok-free.app` for a later step.


## ISE Setup

This demo can be used as an addition to the repository https://github.com/gve-sw/gve_devnet_ise_visitor_management. If you already set up the demo, you can skip this section ("ISE setup") since the required settings are already executed.


#### ISE REST APIs
1. Login to your ISE PAN using the admin or other SuperAdmin user.
2. Navigate to `Administration > System > Settings` and select `API Settings` from the left panel.
3. Navigate to `API Service Settings` and enable the ERS APIs by enabling **ERS (Read/Write)**.
4. Do not enable CSRF unless you know how to use the tokens.
5. Select **Save** to save your changes.
    > The following ISE Administrator Groups allow REST API access:
        * SuperAdmin: Read/Write
        * ERSAdmin: Read/Write
        * ERSOperator: Read Only


#### Create REST API Users
You can use the default ISE admin account for ERS APIs since it has SuperAdmin privileges. However, it is recommended to create separate users with the ERS Admin (Read/Write) or ERS Operator (Read-Only) privileges to use the ERS APIs, so you can separately track and audit their activities.

1. Navigate to `Administration > System > Admin Access`
2. Choose `Administrators > Admin Users` from the left pane
3. Choose `+Add > Create an Admin User` to create a new user with the ers-admin and ers-operator admin groups.

### Create a Sponsor Account

In order to work with guest accounts, you need to set up an additional sponsor account that is able to use the API. Sponsor accounts are needed to perform CRUD operations guest accounts.

1. In ISE, go to `Administration > Identity Management > Identities > Users`   
2. Click `+Add` to add a new user for the ALL_ACCOUNTS user group   
3. This sponsor will have visibility of ALL Guests in the system. If you wanted to limit it then you could use a different group.   
4. Click on `Submit` to save the new account   


### Give the Sponsor Group Access to the API
Under the sponsor group (ALL_ACCOUNTS) add ERS API access permission:

1. In ISE, go to `Work Centers > Guest Access > Portals & Components > Sponsor Groups > ALL_ACCOUNTS`
2. Under `Sponsor Can`, check the box for `Access Cisco ISE guest accounts using the programmatic interface (Guest REST API)`
3. Scroll to the top and click `Save`


### Add Local Location to Guest Locations and Add Guest SSID

The time zone where guests register for your Wi-Fi needs to match your local time zone:

1. In ISE, go to `Work Centers > Guest Access > Settings > Guest Locations and SSIDs`

2. Pick a name for your time zone and select the appropriate entry from the time zone list (e.g. Germany and CET), then scroll to the bottom and click `Save`

3. Add the name of your SSID for guest accounts (e.g. Guest-SSID)


### Create custom fields
Create custom fields in ISE: 

1. Go to: `Work Centers > Guest Access > Settings > Custom Fields > Fill in Custom field name > Choose Data type > Click Add > Click: Save` for the following fields:

* checkedIn
* building
* comment
* hostName
* company
* badgeId

All fields are of type string.


### Access to Sponsor Portal Test Page

1. Go to `Work Centers > Guest Access > Portals & Components > Sponsor Portals > Sponsored Portal (default) > Portal Page Customization > Portal test URL`
2. Use the credentials of the sponsor account created in a previous step (see section "Create a Sponsor Account").
3. Login once to enable the portal.
4. Click on `Manage accounts` to review all accounts. 


## Installation/Configuration

1. Make sure Python 3 and Git are installed in your environment, and if not, you may download Python 3 [here](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) as described [here](https://docs.python.org/3/tutorial/venv.html).
2. Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html)).
3. Access the created virtual environment folder   

    ```cd [add name of virtual environment here]``` 

4. Clone this Github repository:
    ```git clone [add github link here]```
    * For Github link: In Github, click on the clone or download button in the upper part of the page > click the copy icon
    * Or simply download the repository as a zip file using 'Download ZIP' button and extract it
5. Access the downloaded folder:

    ```cd gve_devnet_ise_visitor_management_bot```   

6. Install all dependencies:

    ```pip3 install -r requirements.txt```  

7. Fill in the environment variables in the env. file:

```
LOBBY_USER="<Comma separted list of users with admin privileges>"
BASE_USERS="<Comma separted list of users with base privileges>"

WEBEX_BOT_URL="<Public URL of the running demo code, see section "ngrok">"
WEBEX_BOT_TOKEN="<Bot token, see "Create a Webex Bot" section>"
WEBEX_BOT_EMAIL="<Bot email address, see "Create a Webex Bot" section>"
WEBEX_BOT_APP_NAME="<Bot name, see "Create a Webex Bot" section>"

ISEHOST="https://<ISE hostname/IP>​"

ERS_USERNAME="<ISE username, see "Create REST API Users" section>"
ERS_PASSWORD="<ISE password, see "Create REST API Users" section>"

SPONSOR_USERNAME="<Username of internal user for sponsor portal access. See "Create a Sponsor Account" section>"
SPONSOR_PASSWORD="<Password of internal user for sponsor portal access. See "Create a Sponsor Account" section>"

PORTAL_ID="<ID of sponsor portal, see hint below>"

LOCATION="<Location of the guest users, see "Add Local Location to Guest Locations and Add Guest SSID" section>"
GUEST_SSID_NAME="<Name of the guest SSID to share with visitors, see "Add Local Location to Guest Locations and Add Guest SSID" section>"
```

> Hint: Get a list of all available sponsor portals and their associated IDs by executing  the `sponsorportals.py` script via `python3 sponsorportals.py`.


## Usage

To run the code, use the command:
```
$ python3 bot.py
```

Search the bot based on its bot email within Webex and send a direct message to the bot in the following format:

* **/help** to get help
* **/create** to trigger the process for creating a new ISE guest user
* **/show** to show personal or all visitors based on the account privileges of the user

# Screenshots

![/IMAGES/0image.png](/IMAGES/screenshot.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.