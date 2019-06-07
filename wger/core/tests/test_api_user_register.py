from wger.core.tests.base_testcase import (
    BaseTestCase,
)
from wger.core.tests.api_base_test import ApiBaseTestCase
from rest_framework import status
from django.contrib.auth.models import User
from wger.core.models import UserProfile
from django.urls import reverse

register_url = "/api/v2/user/"


class APIUserRegistrationTestCase(ApiBaseTestCase):
    """ Tests user registration throught the api """
    fixtures = BaseTestCase.fixtures
    full_user = {"username": "apiTest", "password": "testpass"}

    def register_user(self, user=None, ex_status=status.HTTP_201_CREATED):
        """ Helper function for register user"""
        if not user:
            user = self.full_user
        url = register_url
        response = self.client.post(url, user)
        if ex_status == status.HTTP_201_CREATED:
            self.assertEqual(response.status_code, ex_status)
            self.assertEqual(response.data['user']['username'], user['username'].lower())

        else:
            self.assertEqual(response.status_code, ex_status)
        return response

    def test_admin_api_user_create(self):
        """ Test that an admin can create user through the api """

        self.get_credentials(username='admin')
        self.register_user()

    def test_normal_user_cannot_create_user(self):

        self.get_credentials(username='test')
        self.register_user(None, status.HTTP_403_FORBIDDEN)

    def test_normal_user_with_permission_can_create_user(self):
        user = User.objects.get(username="test")
        userprofile = UserProfile.objects.get(user=user)
        userprofile.user_can_create_users = True
        userprofile.save()
        create_user = {"username": "testperms", "password": "adminuser"}
        self.get_credentials(username='test')
        self.register_user(user=create_user)

    def test_register_with_missing_password(self):
        create_user = {"username": "testperms"}
        self.get_credentials(username='admin')
        self.register_user(create_user, status.HTTP_400_BAD_REQUEST)

    def test_register_with_missing_username(self):
        create_user = {"password": "testperms"}
        self.get_credentials("admin")
        self.register_user(create_user, status.HTTP_400_BAD_REQUEST)

        self.get_credentials("admin")


class ApiAssignCreateRoleTestcase(APIUserRegistrationTestCase):
    """Testcase for assigning user create user Permission"""

    fixtures = BaseTestCase.fixtures

    def assign_create_user_role(self, ex_status=status.HTTP_202_ACCEPTED):
        url = reverse('assign-create-users')
        data = {'username': 'test'}

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, ex_status)

    def test_assign_create_user_permission_by_admin(self):
        self.get_credentials("admin")
        self.assign_create_user_role()

    def test_assign_create_user_permission_by_normal_user(self):
        self.get_credentials("test")
        self.assign_create_user_role(status.HTTP_403_FORBIDDEN)

    def test_user_assigned_role_can_add_users(self):
        self.get_credentials("admin")
        self.assign_create_user_role()
        self.client.logout()

        self.client.login(username="test", password="testtest")
        self.register_user()

    def test_assign_create_user_permission_without_data(self):
        url = reverse('assign-create-users')
        data = {}
        self.get_credentials("admin")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
