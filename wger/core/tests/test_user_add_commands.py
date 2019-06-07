from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from wger.core.tests.base_testcase import (
    BaseTestCase,
)
from wger.core.models import UserProfile
from django.contrib.auth.models import User


class AddCreateUserPermissionCommandsTestCase(TestCase, BaseTestCase):

    """Test add permission create """
    fixtures = BaseTestCase.fixtures

    def check_create_user_status(self, status=True, user="test"):
        userobj = User.objects.get(username=user)
        userprofile = UserProfile.objects.get(user=userobj)
        self.assertEqual(userprofile.user_can_create_users, True)

    def test_create_user_permission_add_command(self):
        out = StringIO()
        call_command('add-user-rest-api', "test", stdout=out)
        self.check_create_user_status()

    def test_delete_create_user_permission(self):
        out = StringIO()
        call_command('add-user-rest-api', "test")
        call_command('add-user-rest-api', "test --delete", stdout=out)
        self.check_create_user_status(status=False)

    def test_list_users_with_create_user_permission(self):
        out = StringIO()
        call_command('add-user-rest-api', "test", stdout=out)
        call_command('add-user-rest-api', "test", stdout=out)
        call_command('list-user-rest-api', stdout=out)
