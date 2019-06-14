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
import json

from django.contrib.auth.models import User

from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.utils.helpers import make_token


class WorkoutExportImportTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting importing json
    '''

    def export_json(self):
        '''
        Function for exporting a workout as JSON
        '''
        self.user_login('test')
        user = User.objects.get(username='test')
        uid, token = make_token(user)
        url = '/en/workout/{id}/json/{uuid}/{token}'.format(id=3, uuid=uid, token=token)
        response = self.client.get(url)

        return response

    def test_import_json(self):
        '''
        Function for importing a workout as JSON
        '''
        self.user_login('test')
        user = User.objects.get(username='test')
        uid, token = make_token(user)

        import_data = self.export_json().json()
        url = '/en/workout/json/import'
        content = {}
        content['data'] = json.dumps(import_data, separators=(',', ':'))
        content['workout_id'] = 3
        response = self.client.post(url, data=content)
        self.assertEqual(response.status_code, 200)

    def test_export_json(self):
        response = self.export_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=Workout-3.json')

    def test_import_invalidjson(self):
        '''
        Fuction for importing invalid JSON
        '''

        self.user_login('test')
        user = User.objects.get(username='test')
        uid, token = make_token(user)
        content = {}
        data = {
            "data": "Invalid JSON"
        }
        content['data'] = json.dumps(data, separators=(',', ':'))
        content['workout_id'] = 3
        url = '/en/workout/json/import'
        response = self.client.post(url, data=content)
        self.assertEqual(response.status_code, 400)
