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

from django.urls import reverse
from wger.weight.models import WeightEntry

from wger.core.tests.base_testcase import (
    WorkoutManagerTestCase
)
from unittest import mock

weight_response = {"weight": [{'bmi': 21.53, 'date': '2019-05-27',
                               'logId': 1559001599000, 'source': 'API',
                               'time': '23:59:59', 'weight': 70},
                              {'bmi': 21.23, 'date': '2019-06-01',
                               'logId': 1559433599000, 'source': 'API',
                               'time': '23:59:59', 'weight': 69},
                              {'bmi': 20.61, 'date': '2019-06-15',
                               'logId': 1560643199000, 'source': 'API',
                               'time': '23:59:59', 'weight': 67},
                              {'bmi': 18.76, 'date': '2019-06-16',
                               'logId': 1560729599000, 'source': 'API',
                               'time': '23:59:59', 'weight': 61},
                              {'bmi': 18.76, 'date': '2019-06-17',
                               'logId': 1560815999000, 'source': 'API',
                               'time': '23:59:59', 'weight': 61}]}


class FitbitClientTestCase(WorkoutManagerTestCase):
    '''
    Test the fitbit api client implementation
    '''

    user_success = ('general_manager1',
                    'general_manager2',
                    'manager1')

    def test_fitbit_authorized(self):
        '''
        Tests activating a user as an
        '''
        url = reverse('core:fitbit:fitbit_auth')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_fitbit_get_token(self):
        url = reverse('core:fitbit:fitbit_token') + "?code=4j3jkk32kk2k2k2kk2k3n32k32k3k3k"
        self.user_login("test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


@mock.patch('fitbit.api.Fitbit.get_bodyweight')
class FitbitWeightTestCase(WorkoutManagerTestCase):
    '''
    Test the fitbit api client implementation
    '''

    def test_fitbit_get_weight(self, get_weight_mock):
        '''
        Tests activating a user as an
        '''
        get_weight_mock.return_value = weight_response

        countBefore = WeightEntry.objects.count()
        url = reverse('core:fitbit:fitbit_weight')
        self.user_login("test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        countAfter = WeightEntry.objects.count()
        self.assertGreater(countAfter, countBefore)


class FitbitWeightNoMockTestCase(WorkoutManagerTestCase):
    '''
    Test the fitbit api client implementation
    '''

    def test_fitbit_get_weight(self):
        '''
        Tests activating a user as an
        '''

        countBefore = WeightEntry.objects.count()
        url = reverse('core:fitbit:fitbit_weight')
        self.user_login("test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        countAfter = WeightEntry.objects.count()
        self.assertEqual(countAfter, countBefore)
