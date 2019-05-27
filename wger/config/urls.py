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

from django.urls import path, include

from wger.config.views import language_config
from wger.config.views import gym_config

app_name = "config"
# sub patterns for language configs
patterns_language_config = [
    path(r'<pk>/edit',
        language_config.LanguageConfigUpdateView.as_view(),
        name='edit'),
]


# sub patterns for default gym
patterns_gym_config = [
    path(r'edit',
        gym_config.GymConfigUpdateView.as_view(),
        name='edit'),
]


#
# Actual patterns
#
urlpatterns = [
    path(r'language-config/', include((patterns_language_config, "config"), namespace="language_config")),
    path(r'gym-config/', include((patterns_gym_config, "config"), namespace="gym_config")),
]