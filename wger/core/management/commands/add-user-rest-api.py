from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wger.core.models import UserProfile


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str)
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete permisssion to create user',
        )

    def handle(self, **options):
        for username in options['usernames']:
            try:
                user = User.objects.get(username=username)
                userprofile = UserProfile.objects.get(user=user)

                if options['delete']:
                    userprofile.user_can_create_users = False
                    userprofile.save()
                    print("Permisssion create User Deleted for user {}".format(username))
                    continue

                if userprofile.user_can_create_users:
                    print("User {} already has permission to create users".format(username))
                    continue

                userprofile.user_can_create_users = True
                userprofile.save()
                print("Success, user {} can now create user over the api".format(username))
            except User.DoesNotExist:
                print("User {} does not exist".format(username))
