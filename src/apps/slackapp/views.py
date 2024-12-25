from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from slack_sdk.errors import SlackApiError

# get csrf token
def get_csrf_token(request):
    return JsonResponse(
        {"csrfToken": get_token(request=request)}
    )

# sent message
@require_POST
def send_message(request):
    message = request.POST.get("message")
    channel_id = "C0829PGDX1R"
    try:
        # Call the conversations.list method using the WebClient
        result = app.client.chat_postMessage(
            channel=channel_id,
            text=message
            # You could also use a blocks[] array to send richer content
        )
        # Print result, which includes information about the message (like TS)
        print(result)
        response_message = "Message sent successfully!"

    except SlackApiError as e:
        error_message = e.response['error']
        print(f"Error: {error_message}")
        response_message = f"Failed to send message : {error_message}"
    
    return JsonResponse({"message": response_message})

