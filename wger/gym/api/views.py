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

from rest_framework import viewsets, status
from wger.gym.models import Gym
from wger.gym.api.serializers import GymSerializer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.response import Response


class GymViewSet(viewsets.ModelViewSet, LoginRequiredMixin, PermissionRequiredMixin):
    serializer_class = GymSerializer

    def get_queryset(self):
        '''
        Only allow access to appropriate objects
        '''
        return Gym.objects.all()

    def list(self, request):
        if request.user.has_perm('gym.manage_gyms'):
            return super().list(request)

        return Response({
            "error": "unauthorized"
        }, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        if self.request.user.has_perm('gym.manage_gyms'):
            return super().create(request)

        return Response({
            "error": "unauthorized"
        }, status=status.HTTP_401_UNAUTHORIZED)
