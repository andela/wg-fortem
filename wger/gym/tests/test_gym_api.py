# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from wger.core.tests.api_base_test import ApiBaseTestCase
from rest_framework.views import status
import json
from wger.core.tests.base_testcase import (
    WorkoutManagerTestCase)


class GymApiTest(ApiBaseTestCase, WorkoutManagerTestCase):
    '''
    Test Gym Api
    '''

    def setUp(self):
        super().setUp()
        self.gym_details = {
            "name": "Tevin Thuku",
            "phone": "790561841",
            "email": "bensonnjung39@gmail.com",
            "owner": "kevin",
            "zip_code": "523",
            "city": "Nairobi",
            "street": None
        }

        self.gyms_url = "/api/v2/gym/"

    def create_gym(self, data):
        """Create a gym record """
        return self.client.post(self.gyms_url, data=data)

    def list_gyms(self):
        return self.client.get(self.gyms_url)

    def test_authorized_create_gym(self):
        ''' Test creating a gym by an authorized user'''
        self.user_login("admin")
        response = self.create_gym(data=self.gym_details)
        self.test_scenarios("success", response)

    def test_authorized_view_gym(self):
        self.user_login("admin")
        response = self.list_gyms()
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_create_gym(self):
        ''' Test creating a gym by an unauthorized user'''
        self.user_login("test")
        response = self.create_gym(data=self.gym_details)
        self.test_scenarios("unauthorized", response)

    def test_unauthorized_view_gym(self):
        self.user_login("test")
        response = self.list_gyms()
        self.test_scenarios("unauthorized", response)

    def test_scenarios(self, type=None, response=None):
        if type == "success":
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        elif type == "unauthorized":
            self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
            data = json.loads(response.content.decode('utf-8'))
            self.assertEquals(data["error"], "unauthorized")
