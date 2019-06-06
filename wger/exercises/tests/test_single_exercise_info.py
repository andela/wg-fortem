from wger.core.tests.api_base_test import (ApiGetTestCase, ApiBaseTestCase)
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from rest_framework import status
from wger.exercises.models import Exercise


class TestExerciseInfo(ApiBaseTestCase, ApiGetTestCase, WorkoutManagerTestCase):

    pk = 1
    resource = Exercise
    private_resource = False

    def test_getting_non_existing_exercise(self):
        url2 = 'api/v2/exercise/1000000'
        response = self.client.get(url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
