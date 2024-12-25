import os
import django
from slack_bolt import App
from slack_sdk import WebClient
from django.conf import settings
from django.core.management.base import BaseCommand
from slack_bolt.adapter.socket_mode import SocketModeHandler
from apps.slackapp.slack_handler import register_event_handlers

class Command(BaseCommand):
    help = "Start the Slack Handler"

    def handle(self, *args, **options):
        self._setup_django()
        client = WebClient(token=settings.SLACK_BOT_TOKEN)

        app = App(token=settings.SLACK_BOT_TOKEN)
        register_event_handlers(app, client)

        self._start_socket_mode_handler(app)

    def _setup_django(self):
        if not settings.configured:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
            django.setup

    def _start_socket_mode_handler(self, app):
        try:
            self.stdout.write(self.style.SUCCESS("Starting Slack handler..."))
            print(settings.SLACK_APP_TOKEN)
            print(settings.SLACK_BOT_TOKEN)
            SocketModeHandler(app, settings.SLACK_APP_TOKEN).start()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error starting Socket Mode Handler: {e}"))

