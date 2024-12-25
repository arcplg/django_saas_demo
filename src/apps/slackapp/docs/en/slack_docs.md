# Slack API and Slack Bolt Integration Documentation

This document provides detailed instructions on setting up, configuring, and implementing functionalities to send messages via reactions, commands, workflows, and bot notifications using Slack API and Slack Bolt. It serves as a reference for developers building Slack applications.

---

## 1. Setting Up the Slack Application

### 1.1 Create a New Slack Application
1. Visit the [Slack API App Page](https://api.slack.com/apps) and log in with your Slack credentials.
2. Click **Create New App** and select the **From Scratch** option.
3. Enter the application name and select the workspace where the app will be installed.
4. Click **Create App** to initialize your application.

### 1.2 Configuring OAuth & Permissions
1. Navigate to **OAuth & Permissions** in the app settings menu.
2. Add the following Bot Token Scopes to **Bot Token Scopes**:
   - `app_mentions:read` - Allows the app to read messages that mention the bot.
   - `channels:history` - Grants access to the channel's message history.
   - `channels:read` - Allows viewing channel information.
   - `chat:write` - Allows sending messages to channels or users.
   - `users.profile:read` - Provides access to user profile information in the workspace.
   - `reactions:read` - Allows viewing emoji reactions to messages.
   - `incoming-webhook` - Supports posting messages to specified channels.
3. Save changes to confirm the scopes.
4. Install the application to your workspace by clicking **Install to Workspace**. This action will generate a Bot User OAuth Token (e.g., `xoxb-...`) that will be used for API calls.

### 1.3 Enabling Incoming Webhooks
1. Navigate to **Incoming Webhooks** in the app settings menu.
2. Toggle on **Activate Incoming Webhooks**.
3. Click **Add New Webhook to Workspace**, select a channel, and copy the generated webhook URL.

### 1.4 Configuring Event Subscriptions
1. Go to **Event Subscriptions** in the app settings and enable it.
2. Add a **Request URL** pointing to your server endpoint for handling Slack events. Use a tunneling tool like ngrok during development. (In cases without a **Request URL**, you can use **Socket Mode**)
3. Subscribe to the following **Bot Events**:
   - `reaction_added` - Triggers when a reaction is added to a message.
   - `reaction_removed` - Triggers when a reaction is removed from a message.

## 2. Coding Functionalities

### 2.1 Sending Messages via Reactions
Slack applications can respond to emoji reactions added to messages.

#### Workflow:
1. After adding the bot to channels or the workspace, add Slack reaction icons (e.g., "pe10", "pe50", "pe100", "pe500").
2. Detect the `reaction_added` event using Slack Bolt's event listener.
3. Extract the reaction and user details from the event data.
4. Respond with a custom message using the `say()` function.

#### Example Code add reaction:
```python
from slack_bolt import App

app = App(token="xoxb-your-token")

@app.event("reaction_added")

reaction_set = {"pe10", "pe50", "pe100", "pe500"}

def handle_reaction_added_events(event, say, ack):
    ack()
    reaction = event['reaction']
    sender_id = event['user']
    receiver_id = event['item_user']
    channel_id = event["item"]["channel"]

    if sender_id == receiver_id:
        say(channel=sender_id, text="Bạn không thể thêm pelacoin cho chính bản thân bạn")
        return

    sender = app.client.users_profile_get(user=sender_id)
    sender_name = sender['profile']['real_name']
    receiver = app.client.users_profile_get(user=receiver_id)
    receiver_name = receiver['profile']['real_name']

    data = {
        "receiver_name" : receiver_name,
        "reaction": reaction,
        "receiver_id": receiver_id,
        "sender_name": sender_name,
        "channel_id" : channel_id
    }

    if reaction in reaction_set:
        
        # Handle logic code ...
        
        client.chat_postEphemeral(
            channel=channel_id, 
            user=sender_id, 
            text=f"Cảm ơn bạn đã thêm reaction! Bạn có muốn tặng {reaction} cho {receiver_name} không?", 
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Cảm ơn bạn đã thêm reaction! Bạn có muốn tặng {reaction} cho {receiver_name} không?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "action_id": "reaction_agree",
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Đồng ý"
                            },
                            "style": "primary",
                            "value": json.dumps(data),
                        },
                        {
                            "action_id": "reaction_disagree",
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Không đồng ý"
                            },
                            "style": "danger",
                            "value": "False",
                        }
                    ]
                }
            ]
        )
```

#### Example Code remove reaction:
```python
@app.event("reaction_removed")
def handle_reaction_removed_events(event, say, ack):
    ack()

    reaction = event.get('reaction')

    if reaction in reaction_set:
        print("Reaction removed")
        say(f"Reaction removed {reaction}")
```

### 2.2 Sending Messages via Commands and Workflows
#### Slash Commands
Slash commands allow users to trigger actions by typing commands in Slack (e.g., `/pelacoin`).

1. Define the command in the **Slash Commands** section of your app settings.
2. Implement the command handler using Slack Bolt.
3. Add the Slash Command with the prefix `/pelacoin`.

#### Example Code:
```python
@app.command("/pelacoin")
def handle_pelacoin_command(ack, respond, command, client):
    ack()
    client.views_open(
    trigger_id=command['trigger_id'],
    view={
        "type": "modal",
        "callback_id": "apply_for_leave",
        "title": {
            "type": "plain_text",
            "text": "Concrete-Corp",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Tặng Pelacoin",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Chọn nhân viên tặng point!"
                },
                "accessory": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                        "emoji": True
                    },
                    "action_id": "user_involved"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "10",
                                "emoji": True
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "100",
                                "emoji": True
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "200",
                                "emoji": True
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "checkboxes-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Label",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "reason"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Lý do",
                    "emoji": True
                }
            }
        ]
    })
```

### 2.3 Notifiactions

#### Example Code:
```python
# other code
client.chat_postEphemeral(
    channel=channel_id, 
    user=sender_id, 
    text=f"Cảm ơn bạn đã thêm reaction! Bạn có muốn tặng {reaction} cho {receiver_name} không?", 
    blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Cảm ơn bạn đã thêm reaction! Bạn có muốn tặng {reaction} cho {receiver_name} không?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "action_id": "reaction_agree",
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Đồng ý"
                    },
                    "style": "primary",
                    "value": json.dumps(data),
                },
                {
                    "action_id": "reaction_disagree",
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Không đồng ý"
                    },
                    "style": "danger",
                    "value": "False",
                }
            ]
        }
    ]
)
```

