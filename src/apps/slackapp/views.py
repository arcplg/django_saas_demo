from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import redirect
import requests
from apps.slackapp.models import SlackWorkspace
import json
from django.views.decorators.http import require_GET, require_POST 
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
import time
from django.shortcuts import get_object_or_404
from slack_bolt import App
from slack_sdk import WebClient


def slack_oauth_request(request):
    client_id = settings.SLACK_CLIENT_ID
    redirect_uri = settings.SLACK_REDIRECT_URI
    scope = "app_mentions:read,channels:history,channels:join,channels:read,chat:write,chat:write.customize,chat:write.public,commands,groups:history,groups:read,groups:write,incoming-webhook,reactions:read,users.profile:read"
    user_scope="reactions:read"
    return redirect(f"https://slack.com/oauth/v2/authorize?client_id={client_id}&scope={scope}&user_scope={user_scope}&redirect_uri={redirect_uri}")

def slack_callback(request):
    code = request.GET.get("code", None)
    error = request.GET.get("error", None)

    if error:
        return JsonResponse({"error": f"Slack returned an error: {error}"}, status=400)

    if not code:
        return JsonResponse({"error": "Missing 'code' parameter"}, status=400)
    
    try:
        url = settings.SLACK_OAUTH2_ENDPOINT
        payload = {
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECR,
            "code": code,
            "redirect_uri": settings.SLACK_REDIRECT_URI,
        }
        response = requests.post(url, data=payload)
        response_data = response.json()

        if not response_data.get("ok"):
            return JsonResponse({"error": response_data.get("error", "Unknown error")}, status=400)

        # save workspace infomation
        print(response_data)
        team_id = response_data["team"]["id"]
        team_name = response_data["team"]["name"]
        access_token = response_data["access_token"]
        bot_user_id = response_data["bot_user_id"]
        user_id = response_data["authed_user"]["id"]
        channel_id = response_data["incoming_webhook"]["channel_id"]

        # Save db
        SlackWorkspace.objects.update_or_create(
            team_id=team_id,
            defaults={
                "user_id": user_id,
                "channel_id": channel_id,
                "team_name": team_name,
                "access_token": access_token,
                "bot_user_id": bot_user_id
            }
        )

        return redirect("/slack/callback/success")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def save_workspace_info(data):
    SlackWorkspace.objects.update_or_create(data)
    print("Workspace saved:", data)

def slack_callback_success(request):
    return HttpResponse("Bot installed successfully!")

def verify_slack_request(request):
    slack_signature = request.headers.get("X-Slack-Signature")
    slack_request_timestamp = request.headers.get("X-Slack-Request-Timestamp")

    if not slack_signature or not slack_request_timestamp:
        return JsonResponse({"error": "Missing Slack signature or timestamp"}, status=403)
    
    if abs(time.time() - int(slack_request_timestamp)) > 60 * 5:
        return JsonResponse({"error": "Request timestamp expired"}, status=403)
    
    body = request.body.decode("utf-8")
    basestring = f"v0:{slack_request_timestamp}:{body}"
    my_signature = "v0=" + hmac.new(
        settings.SLACK_SIGNING_SECR.encode(),
        basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(my_signature, slack_signature):
        return JsonResponse({"error": "Invalid signature"}, status=403)
    
    return None

@require_POST
@csrf_exempt
def slack_events(request):
    verification_response = verify_slack_request(request)
    if verification_response:
        return verification_response

    try: 
        data = json.loads(request.body)

        if data.get("type") == "url_verification":
            return JsonResponse({"challenge": data.get("challenge")})

        team_id = data.get('team_id')
        print("team_id", team_id)
        workspace = get_object_or_404(SlackWorkspace, team_id=team_id)
        
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            reaction_set = { "pe10", "pe50", "pe100", "pe500" }
            reaction = event.get("reaction")
            user = event.get("user")
            item = event.get("item", {})
            channel = item.get("channel")
            receiver_id = event['item_user']

            if reaction in reaction_set:
                if event.get("type") == "reaction_added":
                    client = WebClient(token=workspace.access_token)
                    app = App(token=workspace.access_token)

                    user_response = client.users_info(user=user)
                    if not user_response.get("ok"):
                        return JsonResponse({"challenge": data.get("challenge")})
                    
                    user_info = user_response.get("user", {})
                    receiver_name = user_info.get("real_name")

                    if user == receiver_id:
                        client.chat_postMessage(
                            channel=user,
                            text="You cannot received pelacoin from your self"
                        )
                        return JsonResponse({"message": "Error: Self-reaction detected"}, status=200)
                    
                    client.chat_postEphemeral(
                        channel=channel, 
                        user=user, 
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
                    print(f"Reaction added by {user}: {reaction} in channel {channel}")

                    return JsonResponse({"message": "Reaction added event received"}, status=200)
                
                if event.get("type") == "reaction_removed":
                    print(f"Reaction removed by {user}: {reaction} in channel {channel}")

                    return JsonResponse({"message": "Reaction removed event received"}, status=200)

        if "challenge" in data:
            return JsonResponse({"challenge": data["challenge"]})
        return JsonResponse({"message": "Invalid request"}, status=400) 
    except: 
        return JsonResponse({'error': 'Server error'}, status=500)
