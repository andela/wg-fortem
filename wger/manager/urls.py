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
from django.contrib.auth.decorators import login_required
from django.urls import path
from wger.manager.views import (
    pdf,
    schedule,
    schedule_step,
    ical,
    workout,
    log,
    set,
    day,
    workout_session,
    json
)

app_name = "manager"
# sub patterns for workout logs
patterns_log = [
    path('<pk>/view',
         log.WorkoutLogDetailView.as_view(),
         name='log'),
    path('<pk>/edit',  # JS
         log.WorkoutLogUpdateView.as_view(),
         name='edit'),
    path('<pk>/delete',
         log.WorkoutLogDeleteView.as_view(),
         name='delete')
]


# sub patterns for workouts
patterns_workout = [
    path('overview',
         workout.overview,
         name='overview'),
    path('add',
         workout.add,
         name='add'),
    path('<pk>/copy/',
         workout.copy_workout,
         name='copy'),
    path('<pk>/edit/',
         workout.WorkoutEditView.as_view(),
         name='edit'),
    path('<pk>/delete/',
         workout.WorkoutDeleteView.as_view(),
         name='delete'),
    path('<pk>/view/',
         workout.view,
         name='view'),
    url(r'^calendar/(?P<username>[\w.@+-]+)$',
        log.calendar,
        name='calendar'),
    path('calendar',
         log.calendar,
         name='calendar'),
    url(r'^calendar/(?P<username>[\w.@+-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})$',
        log.calendar,
        name='calendar'),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{1,2})$',
        log.calendar,
        name='calendar'),
    url(r'^calendar/(?P<username>[\w.@+-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$',
        log.day,
        name='calendar-day'),
    url(r'^(?P<pk>\d+)/ical/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        ical.export,
        name='ical'),
    path('<pk>/ical',
         ical.export,
         name='ical'),
    url(r'^(?P<id>\d+)/pdf/log/(?P<images>[01]+)/(?P<comments>[01]+)/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        pdf.workout_log,
        name='pdf-log'),  # JS!
    url(r'^(?P<id>\d+)/pdf/log/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        pdf.workout_log,
        name='pdf-log'),
    url(r'^(?P<id>\d+)/pdf/log/(?P<images>[01]+)/(?P<comments>[01]+)$',
        pdf.workout_log,
        name='pdf-log'),
    path('<id>/pdf/log',
         pdf.workout_log,
         name='pdf-log'),
    url(r'^(?P<id>\d+)/pdf/table/(?P<images>[01]+)/(?P<comments>[01]+)/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        pdf.workout_view,
        name='pdf-table'),  # JS!
    url(r'^(?P<id>\d+)/pdf/table/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        pdf.workout_view,
        name='pdf-table'),
    url(r'^(?P<id>\d+)/pdf/table/(?P<images>[01]+)/(?P<comments>[01]+)$',
        pdf.workout_view,
        name='pdf-table'),
    path('<id>/pdf/table',
         pdf.workout_view,
         name='pdf-table'),
    path('<day_pk>/timer',
         workout.timer,
         name='timer'),
    path('<id>/json/<uidb64>/<token>',
         json.export_workout,
         name='export-workout'),
    path('json/import',
         json.Importworkout.as_view(), name='import-workout')
]


# sub patterns for workout sessions
patterns_session = [
    url(r'^(?P<workout_pk>\d+)/add/(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$',
        workout_session.WorkoutSessionAddView.as_view(),
        name='add'),
    path('<pk>/edit',
         workout_session.WorkoutSessionUpdateView.as_view(),
         name='edit'),
    url(r'^(?P<pk>\d+)/delete/(?P<logs>(session|logs))?$',
        workout_session.WorkoutSessionDeleteView.as_view(),
        name='delete'),
]


# sub patterns for workout days
patterns_day = [
    path('<pk>/edit/',
         login_required(day.DayEditView.as_view()),
         name='edit'),
    path('<workout_pk>/day/add/',
         login_required(day.DayCreateView.as_view()),
         name='add'),
    path('<pk>/delete/',
         day.delete,
         name='delete'),
    path('<id>/view/',
         day.view,
         name='view'),
    path('<pk>/log/add/',
         log.add,
         name='log'),
]

# sub patterns for workout sets
patterns_set = [
    path('day/<day_pk>/set/add/',
         set.create,
         name='add'),
    path('get-formset/<exercise_pk>/<reps>/',
         set.get_formset,
         name='get-formset'),  # Used by JS
    path('<pk>/delete',
         set.delete,
         name='delete'),
    path('<pk>/edit/',
         set.edit,
         name='edit'),
]


# sub patterns for schedules
patterns_schedule = [
    path('overview',
         schedule.overview,
         name='overview'),
    path('add',
         schedule.ScheduleCreateView.as_view(),
         name='add'),
    path('<pk>/view/',
         schedule.view,
         name='view'),
    path('<pk>/start',
         schedule.start,
         name='start'),
    path('<pk>/edit/',
         schedule.ScheduleEditView.as_view(),
         name='edit'),
    path('<pk>/delete/',
         schedule.ScheduleDeleteView.as_view(),
         name='delete'),
    url(r'^(?P<pk>\d+)/ical/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        ical.export_schedule,
        name='ical'),
    path('<pk>/ical',
         ical.export_schedule,
         name='ical'),

    url(
        r'^(?P<pk>\d+)/pdf/log/(?P<images>[01]+)/(?P<comments>[01]+)/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        schedule.export_pdf_log,
        name='pdf-log'),  # JS!
    url(r'^(?P<pk>\d+)/pdf/log/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        schedule.export_pdf_log,
        name='pdf-log'),
    url(r'^(?P<pk>\d+)/pdf/log/(?P<images>[01]+)/(?P<comments>[01]+)$',
        schedule.export_pdf_log,
        name='pdf-log'),
    path('<pk>/pdf/log',
         schedule.export_pdf_log,
         name='pdf-log'),
    url(
        r'^(?P<pk>\d+)/pdf/table/(?P<images>[01]+)/(?P<comments>[01]+)/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        schedule.export_pdf_table,
        name='pdf-table'),  # JS!
    url(r'^(?P<pk>\d+)/pdf/table/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        schedule.export_pdf_table,
        name='pdf-table'),
    url(r'^(?P<pk>\d+)/pdf/table/(?P<images>[01]+)/(?P<comments>[01]+)$',
        schedule.export_pdf_table,
        name='pdf-table'),
    path('<pk>/pdf/table',
         schedule.export_pdf_table,
         name='pdf-table'),
]


# sub patterns for schedule steps
patterns_step = [
    path('<schedule_pk>/step/add',
         schedule_step.StepCreateView.as_view(),
         name='add'),
    path('<pk>/edit',
         schedule_step.StepEditView.as_view(),
         name='edit'),
    path('<pk>/delete',
         schedule_step.StepDeleteView.as_view(),
         name='delete'),
]


urlpatterns = [
    path('', include((patterns_workout, 'workout'), namespace="workout")),
    path('log/', include((patterns_log, 'log'), namespace="log")),
    path('day/', include((patterns_day, 'day'), namespace="day")),
    path('set/', include((patterns_set, 'set'), namespace="set")),
    path('session/', include((patterns_session, "session"), namespace="session")),
    path('schedule/', include((patterns_schedule, 'schedule'), namespace="schedule")),
    path('schedule/step/', include((patterns_step, "step"), namespace="step")),
]
