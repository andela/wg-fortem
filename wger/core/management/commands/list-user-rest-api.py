from django.core.management.base import BaseCommand
from wger.core.models import UserProfile


class Command(BaseCommand):

    def handle(self, **options):
        users = UserProfile.objects.filter(user_can_create_users=True)
        for user in users:
            print(user.user.username)
