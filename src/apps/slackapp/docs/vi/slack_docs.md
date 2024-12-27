# Tài liệu tích hợp Slack API và Slack Bolt

Tài liệu này cung cấp hướng dẫn chi tiết về thiết lập, cấu hình và triển khai các chức năng để gửi tin nhắn qua phản ứng, command, quy trình làm việc và thông báo bot bằng Slack API và Slack Bolt. Tài liệu này được thiết kế như một tài liệu tham khảo cho các nhà phát triển xây dựng ứng dụng Slack.

---

## 1. Thiết lập ứng dụng trong slack

### 1.1 Tạo ứng dụng Slack mới
1. Truy cập [trang Ứng dụng Slack API](https://api.slack.com/apps) và đăng nhập bằng thông tin đăng nhập Slack của bạn.
2. Click **Create New App** và chọn tùy chọn **From Scratch**.
3. Nhập tên ứng dụng và chọn workspace nơi ứng dụng sẽ được cài đặt.
4. Click **Create App** để khởi tạo ứng dụng của bạn.

### 1.2 Configuring OAuth & Permissions
1. Điều hướng đến **OAuth & Permissions** trong menu cài đặt ứng dụng.
2. Thêm các phạm vi Bot Token Scopes sau đây vào **Bot Token Scopes**:
   - `app_mentions:read` - Cho phép ứng dụng đọc tin nhắn có nhắc đến bot.
   - `channels:history` - Cho phép truy cập vào lịch sử tin nhắn channels.
   - `channels:read` - Cấp quyền xem thông tin channels.
   - `chat:write` - Cho phép gửi tin nhắn đến các channels hoặc người dùng.
   - `users.profile:read` - Cung cấp quyền truy cập vào hồ sơ người dùng workspace làm việc.
   - `reactions:read` - Cho phép xem phản ứng biểu tượng cảm xúc trên tin nhắn.
   - `incoming-webhook` - Hỗ trợ đăng tin nhắn lên các kênh đã chỉ định.
   - `groups:write` - Quản lý các kênh riêng tư mà bot đã được thêm vào và tạo các kênh mới.
   - `users:read` - Xem mọi người trong không gian làm việc.
   - `usergroups:read` - Xem nhóm người dùng trong workspace.
   - `im:history` - Xem tin nhắn và nội dung khác trong tin nhắn trực tiếp mà bot đã được thêm vào.
   - `groups:read` - Xem thông tin cơ bản về các kênh riêng tư mà bot đã được thêm vào.
   - `groups:history` - Xem tin nhắn và nội dung khác trong các kênh riêng tư mà bot đã được thêm vào.
   - `commands` - Thêm phím tắt / hoặc lệnh gạch chéo mà mọi người có thể sử dụng.
3. Lưu thay đổi để xác nhận scopes.
4. Cài đặt ứng dụng vào workspace của bạn bằng cách nhấp vào **Install to Workspace**. Thao tác này sẽ tạo một Bot User OAuth Token (e.g., `xoxb-...`) sẽ được sử dụng cho các lệnh gọi API.

### 1.3 Enabling Incoming Webhooks
1. Điều hướng đến **Incoming Webhooks** trong menu cài đặt ứng dụng.
2. Bật **Activate Incoming Webhooks**.
3. Click **Add New Webhook to Workspace**, chọn một channels và sao chép URL webhook đã tạo.

### 1.4 Configuring Event Subscriptions
1. Đi đến **Event Subscriptions** trong cài đặt app và bật nó.
2. Thêm một **Request URL** trỏ đến điểm cuối server của bạn để xử lý các sự kiện Slack. Sử dụng công cụ tunneling tool như ngrok trong quá trình phát triển. (Trường hợp không có **Request URL** có thể sử dụng **Socket Mode**)
    - Thêm Request URL: `https://polliwog-above-mentally.ngrok-free.app/slack/events`
    - Tại source thêm api để lắng nghe sự kiện `slack/events`
```python
@require_POST
@csrf_exempt
def slack_events(request):
    verification_response = verify_slack_request(request)
    if verification_response:
        return verification_response

    try: 
        # code logic

        if "challenge" in data:
            return JsonResponse({"challenge": data["challenge"]})
        return JsonResponse({"message": "Invalid request"}, status=400) 
    except: 
        return JsonResponse({'error': 'Server error'}, status=500)
```

3. Đăng ký các sự kiện sau **Bot Events**:
   - `reaction_added` - Kích hoạt khi reaction được thêm vào tin nhắn.
   - `reaction_removed` - Kích hoạt khi reaction được xóa ở tin nhắn.

## 2. Coding Functionalities

### 2.1 Sending Messages via Reactions
Ứng dụng Slack có thể phản hồi các reaction biểu tượng cảm xúc được thêm vào tin nhắn.

#### Workflow:
1. Sau khi thêm bot vào channels hoặc workspace thì thêm các reaction icon của slack. Ví dụ: "pe10", "pe50", "pe100", "pe500" 
2. Phát hiện sự kiện `reaction_added` bằng trình lắng nghe sự kiện của Slack Bolt's.
3. Trích xuất reaction và thông tin chi tiết của người dùng từ dữ liệu sự kiện.
4. Phản hồi bằng tin nhắn tùy chỉnh bằng hàm `say()`.

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

### 2.2 Gửi tin nhắn qua lệnh và Workflows
#### Slash Commands
Slash commands cho phép người dùng kích hoạt hành động bằng cách nhập lệnh trong Slack (e.g., `/pelacoin`).

1. Xác định lệnh trong **Slash Commands** phần cài đặt ứng dụng.
2. Triển khai trình xử lý lệnh bằng cách sử dụng Slack Bolt.
3. Thêm Slash Commands với ký hiệu `/pelacoin` 

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

### 2.3 Thông báo đến người dùng

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

### 3. Manage Distribution

