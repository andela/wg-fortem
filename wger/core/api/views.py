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

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404


from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit,
    UserApiLog)
from wger.core.api.serializers import (
    UsernameSerializer,
    LanguageSerializer,
    DaysOfWeekSerializer,
    LicenseSerializer,
    RepetitionUnitSerializer,
    WeightUnitSerializer
)
from wger.core.api.serializers import (
    UserprofileSerializer, UserRegistrationSerializer)
from wger.utils.permissions import UpdateOnlyPermission, WgerPermission


from django.utils import translation
from wger.utils.permissions import AllowCreateUserPermission
from rest_framework.views import APIView
from rest_framework import permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for workout objects
    '''
    is_private = True
    serializer_class = UserprofileSerializer
    permission_classes = (WgerPermission, UpdateOnlyPermission)
    ordering_fields = '__all__'

    def get_queryset(self):
        '''
        Only allow access to appropriate objects
        '''
        return UserProfile.objects.filter(user=self.request.user)

    def get_owner_objects(self):
        '''
        Return objects to check for ownership permission
        '''
        return [(User, 'user')]

    @detail_route()
    def username(self, request, pk):
        '''
        Return the username
        '''

        user = self.get_object().user
        return Response(UsernameSerializer(user).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name')


class DaysOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = DaysOfWeek.objects.all()
    serializer_class = DaysOfWeekSerializer
    ordering_fields = '__all__'
    filter_fields = ('day_of_week', )


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name',
                     'url')


class RepetitionUnitViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for repetition units objects
    '''
    queryset = RepetitionUnit.objects.all()
    serializer_class = RepetitionUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class WeightUnitViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for weight units objects
    '''
    queryset = WeightUnit.objects.all()
    serializer_class = WeightUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (AllowCreateUserPermission | permissions.IsAdminUser,)

    def post(self, request):
        if request.data.get('username', None):
            request.data['username'] = request.data['username'].lower()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = User.objects.create_user(username, email, password)
        user.save()
        serializer.instance = user
        language = Language.objects.get(short_name=translation.get_language())
        user.userprofile.notification_language = language
        user.userprofile.save()
        apiLog = UserApiLog(user=user, created_by=request.user)
        apiLog.save()

        return Response({"user": serializer.data, "message": "Success User created"},
                        status=status.HTTP_201_CREATED)


class AssignCreateUserPermission(APIView):
    """ Set permission for user to create other users"""
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        username = request.data.get("username", None)
        if username:

            user = get_object_or_404(User, username=username)
            user.userprofile.user_can_create_users = True
            user.userprofile.save()
            return Response({"Message": "Success User {} can Create user".format(username)},
                            status.HTTP_202_ACCEPTED)
        return Response({"Error": "username is Required"}, status=status.HTTP_400_BAD_REQUEST)
