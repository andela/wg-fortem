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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.decorators import login_required

from wger.exercises.views import (
    exercises,
    comments,
    categories,
    muscles,
    images,
    equipment
)


app_name = "exercises"
# sub patterns for muscles
patterns_muscle = [
    path('overview/',
        muscles.MuscleListView.as_view(),
        name='overview'),
    path('admin-overview/',
        muscles.MuscleAdminListView.as_view(),
        name='admin-list'),
    path('add/',
        muscles.MuscleAddView.as_view(),
        name='add'),
    path('<pk>/edit/',
        muscles.MuscleUpdateView.as_view(),
        name='edit'),
    path('<pk>/delete/',
        muscles.MuscleDeleteView.as_view(),
        name='delete'),
]

# sub patterns for exercise images
patterns_images = [
    path('<exercise_pk>/image/add',
        images.ExerciseImageAddView.as_view(),
        name='add'),
    path('<pk>/edit',
        images.ExerciseImageEditView.as_view(),
        name='edit'),
    path('<exercise_pk>/image/<pk>/delete',
        images.ExerciseImageDeleteView.as_view(),
        name='delete'),
    path('<pk>/accept/',
        images.accept,
        name='accept'),
    path('(<pk>/decline/',
        images.decline,
        name='decline'),
]

# sub patterns for exercise comments
patterns_comment = [
    path('<exercise_pk>/comment/add/',
        comments.ExerciseCommentAddView.as_view(),
        name='add'),
    path('<pk>/edit/',
        comments.ExerciseCommentEditView.as_view(),
        name='edit'),
    path('<id>/delete/',
        comments.delete,
        name='delete'),
]

# sub patterns for categories
patterns_category = [
    path('list',
        categories.ExerciseCategoryListView.as_view(),
        name='list'),
    path('<pk>/edit/',
        categories.ExerciseCategoryUpdateView.as_view(),
        name='edit'),
    path('add/',
        categories.ExerciseCategoryAddView.as_view(),
        name='add'),
    path('<pk>/delete/',
        categories.ExerciseCategoryDeleteView.as_view(),
        name='delete'),
]

# sub patterns for equipment
patterns_equipment = [
    path('list',
        equipment.EquipmentListView.as_view(),
        name='list'),
    path('add',
        equipment.EquipmentAddView.as_view(),
        name='add'),
    path('<pk>/edit',
        equipment.EquipmentEditView.as_view(),
        name='edit'),
    path('<pk>/delete',
        equipment.EquipmentDeleteView.as_view(),
        name='delete'),
    path('overview',
        equipment.EquipmentOverviewView.as_view(),
        name='overview'),
]


# sub patterns for exercises
patterns_exercise = [
    path('overview/',
        exercises.ExerciseListView.as_view(),
        name='overview'),
    path('<id>/view/',
        exercises.view,
        name='view'),
    url(r'^(?P<id>\d+)/view/(?P<slug>[-\w]*)/?$',
        exercises.view,
        name='view'),      
    path('add/',
        login_required(exercises.ExerciseAddView.as_view()),
        name='add'),
    path('<pk>/edit/',
        exercises.ExerciseUpdateView.as_view(),
        name='edit'),
    path('<pk>/correct',
        exercises.ExerciseCorrectView.as_view(),
        name='correct'),
    path('<pk>/delete/',
        exercises.ExerciseDeleteView.as_view(),
        name='delete'),
    path('pending/',
        exercises.PendingExerciseListView.as_view(),
        name='pending'),
    path('<pk>/accept/',
        exercises.accept,
        name='accept'),
    path('<pk>/decline/',
        exercises.decline,
        name='decline'),
]


urlpatterns = [
    path('muscle/', include((patterns_muscle, "exercises"), namespace="muscle")),
    path('image/', include((patterns_images, "exercises"), namespace="image")),
    path('comment/', include((patterns_comment, "exercises"), namespace="comment")),
    path('category/', include((patterns_category, "exercises"), namespace="category")),
    path('equipment/', include((patterns_equipment, "exercises"), namespace="equipment")),
    path('', include((patterns_exercise, "exercises"), namespace="exercise")),
]
