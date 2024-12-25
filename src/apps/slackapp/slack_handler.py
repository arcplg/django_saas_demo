import logging
from slack_bolt import App
from slack_sdk import WebClient
from django.conf import settings
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import json
from collections import defaultdict

def register_event_handlers(app, client):
    reaction_set = { "pe10", "pe50", "pe100", "pe500" }
    actions_used = defaultdict(lambda: defaultdict(list))
    
    @app.event("reaction_added")
    def handle_reaction_added_events(event, say, ack):
        ack()
        reaction = event['reaction']
        sender_id = event['user']
        receiver_id = event['item_user']
        channel_id = event["item"]["channel"]

        if sender_id == receiver_id:
            say(channel=sender_id, text="You cannot received pelacoin from your self")
            return

        print(sender_id)
        print(receiver_id)

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
            print(reaction)
            print("Reaction added")

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

            # say(f"Hi {receiver_name}, you received coin {reaction} from {sender_name}")
            # say(channel=sender_id, text=f"Bạn vừa gửi tặng {reaction} đến người nhận {receiver_name}")
            # say(channel=receiver_id, text=f"Bạn vừa được thêm {reaction} coin từ {sender_name}")


    @app.action("reaction_agree") 
    def handle_agree(ack, body, client, say): 
        ack() 
        print("asdasd")
        try:
            action = body.get("actions", [])[0] if body.get("actions") else None
            if action: 
                json_data = action.get("value")
                data = json.loads(json_data)
                reaction = data['reaction']
                receiver_name = data['receiver_name']
                receiver_id = data['receiver_id']
                sender_name = data['sender_name']
                sender_id = body.get('user', {}).get('id')
                channel_id = data.get('channel_id')

                if body['container']['message_ts'] in actions_used[channel_id][sender_id]:
                    client.chat_postEphemeral(
                        channel=channel_id, 
                        user=sender_id, 
                        text=f"Thao tác này đã được thực hiện trước đó",
                    )
                    return
                
                actions_used[channel_id][sender_id].append(body['container']['message_ts'])


                say(channel=sender_id, text=f"Bạn vừa gửi tặng {reaction} đến người nhận {receiver_name}")
                say(channel=receiver_id, text=f"Bạn vừa được thêm {reaction} coin từ {sender_name}")
        except SlackApiError as e:
            print(f"Error starting Socket Mode Handler: {e}")
        except (json.JSONDecodeError, IndexError, AttributeError) as e:
            print(f"Error processing action data: {e}")
        except KeyError as e:
            print(f"Key Error: {e}")
            
    @app.action("reaction_disagree") 
    def handle_disagree(ack, body, client): 
        ack() # Xử lý không đồng ý 
        print("User disagreed with the reaction.")   

    @app.event("reaction_removed")
    def handle_reaction_removed_events(event, say, ack):
        ack()

        reaction = event.get('reaction')

        if reaction in reaction_set:
            print(reaction)
            print("Reaction removed")
            say(f"Reaction removed {reaction}")

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
        respond(f"{command['text']}")
