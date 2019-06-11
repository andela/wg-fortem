# -*- coding: utf-8 -*-

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

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from wger.manager.models import Workout, Day, Set, Exercise, Setting
from wger.core.models import DaysOfWeek
from wger.utils.helpers import check_token


def export_workout(request, id, uidb64=None, token=None):

    # Get the workout
    if uidb64 is not None and token is not None:
        if check_token(uidb64, token):
            workout = get_object_or_404(Workout, pk=id)
        else:
            return HttpResponseForbidden()
    else:
        if request.user.is_anonymous():
            return HttpResponseForbidden()
        workout = get_object_or_404(Workout, pk=id, user=request.user)

    if len(workout.canonical_representation['day_list']) > 0:

        exercise_set = workout.canonical_representation['day_list'][0]['set_list']
        workout_details = {
            'description': workout.canonical_representation['day_list'][0]['obj'].description,
            'workout_days': workout.canonical_representation['day_list'][0]['days_of_week']['text']
        }

        set_list = []
        for set in exercise_set:
            set_dict = {}
            exercise_list = []
            holder = {}
            set_dict['set_id'] = set['obj'].id
            set_dict['set_order'] = set['obj'].order
            set_dict['sets'] = set['obj'].sets
            set_dict['excerciseday_id'] = set['obj'].exerciseday_id
            for item in set['exercise_list']:
                holder['name_of_exercise'] = item['obj'].name
                holder['description'] = item['obj'].description
                holder['category_id'] = item['obj'].category_id
                holder['license_id'] = item['obj'].license_id
                holder['author'] = item['obj'].Author_id
                holder['settings_list'] = item['setting_list']
                repetition_list = [repetition.name for repetition in item['repetition_units']]
                weight_units = [unit.name for unit in item['weight_units']]
                holder['weight_units'] = weight_units
                holder['repetition_list'] = repetition_list
                holder['comments'] = item['comment_list']
                holder['reps'] = item['setting_obj_list'][0].reps
                holder['order'] = item['setting_obj_list'][0].order
                exercise_list.append(holder)

            set_dict['muscles'] = set['muscles']
            set_dict['exercise_list'] = exercise_list

            set_list.append(set_dict)

        workout_details['set_list'] = set_list
    else:
        workout_details = []

    json_data = json.dumps(workout_details)

    # Create the HttpResponse object with appropriate JSON headers
    response = HttpResponse(json_data, content_type='application/json')

    response['Content-Disposition'] = 'attachment; filename=Workout-{0}.json'.format(id)
    response['Content-Length'] = len(response.content)
    return response


class Importworkout(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        try:
            content = request.data
            data = json.loads(content['data'])
            workout = get_object_or_404(Workout, pk=content['workout_id'])
            workout.user = request.user
            workout.comment = data['description']
            workout.save()
            days = data['workout_days'].split(', ')
            days_of_week = DaysOfWeek.objects.filter(day_of_week__in=days)
            day_save = Day.objects.create(training=workout, description=data['description'])
            day_save.day.set(days_of_week)
            set_list = data['set_list']
            for set in set_list:
                no_of_sets = set['sets']
                exercise_names = [exercise['name_of_exercise'] for exercise in set['exercise_list']]
                exercises = Exercise.objects.filter(name__in=exercise_names)
                for exercise in exercises:
                    exercise_in_list = next((item for item in set['exercise_list']
                                             if item['name_of_exercise'] == exercise.name), {})
                    reps = exercise_in_list.get('reps', 0)
                    order = exercise_in_list.get('order', 1)
                    day_set = Set(exerciseday=day_save, sets=no_of_sets, order=set['set_order'])
                    day_set.save()
                    day_set.exercises.add(exercise)
                    settings = Setting(set=day_set, exercise=exercise,
                                       reps=reps, order=order)
                    settings.save()

            return HttpResponse(data)
        except KeyError:
            return Response(
                data={"error": "Ooops! Something went wrong. Verify that your JSON file is valid"},
                status=status.HTTP_400_BAD_REQUEST
            )
