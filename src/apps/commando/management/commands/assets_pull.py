import helpers
from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings

STATICFILES_ASSETS_DIR = getattr(settings, 'STATICFILES_ASSETS_DIR')

ASSETS_STATICFILES = {
    "saas-theme.min.css": "https://raw.githubusercontent.com/codingforentrepreneurs/SaaS-Foundations/main/src/staticfiles/theme/saas-theme.min.css",
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map"
}

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading assets static files")
        complated_urls = []
        for name, url in ASSETS_STATICFILES.items():
            out_path = STATICFILES_ASSETS_DIR / name
            dl_success = helpers.download_to_local(url, out_path)
            if dl_success:
                complated_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to download {url}')
                )
        if set(complated_urls) == set(ASSETS_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS('Successfully updated all vendor static files.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Some files were not updated.')
            )