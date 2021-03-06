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


from django.conf.urls import (
    url,
    include
)
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from wger.core.views import (
    user,
    misc,
    license,
    languages,
    repetition_units,
    weight_units


)
from wger.core.forms import (
    UserLoginForm)
from wger.core.views import fitbit_client

app_name = "core"
# sub patterns for languages
patterns_language = [
    path("list",
         languages.LanguageListView.as_view(),
         name='overview'),
    path("<int:pk>/view",
         languages.LanguageDetailView.as_view(),
         name="view"),
    path("<int:pk>/delete",
         languages.LanguageDeleteView.as_view(),
         name='delete'),
    path("<int:pk>/edit",
         languages.LanguageEditView.as_view(),
         name='edit'),
    path("add",
         languages.LanguageCreateView.as_view(),
         name='add'),
]

# sub patterns for user
patterns_user = [
    path("login",
         LoginView.as_view(template_name='user/login.html', authentication_form=UserLoginForm),
         name='login'),
    path("logout",
         user.logout,
         name='logout'),
    path("delete",
         user.delete,
         name='delete'),
    path("<int:user_pk>/delete",
         user.delete,
         name='delete'),
    path("<int:user_pk>/trainer-login",
         user.trainer_login,
         name='trainer-login'),
    path("registration",
         user.registration,
         name='registration'),
    path("preferences",
         user.preferences,
         name='preferences'),
    path("api-key",
         user.api_key,
         name='api-key'),
    path("demo-entries",
         misc.demo_entries,
         name='demo-entries'),
    path("<int:pk>/activate",
         user.UserActivateView.as_view(),
         name='activate'),
    path("<int:pk>/deactivate",
         user.UserDeactivateView.as_view(),
         name='deactivate'),
    path('<int:pk>/edit',
         user.UserEditView.as_view(),
         name='edit'),
    path('<pk>/overview',
         user.UserDetailView.as_view(),
         name='overview'),
    path('list',
         user.UserListView.as_view(),
         name='list'),

    # Password reset is implemented by Django, no need to cook our own soup here
    # (besides the templates)
    path('password/change',
         views.PasswordChangeView.as_view(
             success_url=reverse_lazy('core:user:password_change_done')),
         {'template_name': 'user/change_password.html',
          'post_change_redirect': reverse_lazy('core:user:preferences')},
         name='change-password'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password/reset/',
         views.PasswordResetView.as_view(),
         {'template_name': 'user/password_reset_form.html',
          'email_template_name': 'user/password_reset_email.html',
          'post_reset_redirect': reverse_lazy('core:user:password_reset_done')},
         name='password_reset'),
    path('password/reset/done/',
         views.PasswordResetDoneView.as_view(),
         {'template_name': 'user/password_reset_done.html'},
         name='password_reset_done'),
    url(r'^password/reset/check/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        views.PasswordResetConfirmView.as_view(),
        {'template_name': 'user/password_reset_confirm.html',
         'post_reset_redirect': reverse_lazy('core:user:password_reset_complete')},
        name='password_reset_confirm'),
    path('password/reset/complete/',
         views.PasswordResetCompleteView.as_view(),
         {'template_name': 'user/password_reset_complete.html'},
         name='password_reset_complete'),
]


# sub patterns for licenses
patterns_license = [
    path('license/list',
         license.LicenseListView.as_view(),
         name='list'),
    path('license/add',
         license.LicenseAddView.as_view(),
         name='add'),
    path('license/<int:pk>/edit',
         license.LicenseUpdateView.as_view(),
         name='edit'),
    path('license/<int:pk>/delete',
         license.LicenseDeleteView.as_view(),
         name='delete'),
]

# sub patterns for setting units
patterns_repetition_units = [
    path('list',
         repetition_units.ListView.as_view(),
         name='list'),
    path('add',
         repetition_units.AddView.as_view(),
         name='add'),
    path('<int:pk>/edit',
         repetition_units.UpdateView.as_view(),
         name='edit'),
    path('<int:pk>/delete',
         repetition_units.DeleteView.as_view(),
         name='delete'),
]

# sub patterns for setting units
patterns_weight_units = [
    path('list',
         weight_units.ListView.as_view(),
         name='list'),
    path('add',
         weight_units.AddView.as_view(),
         name='add'),
    url(r'^(?P<pk>\d+)/edit',
        weight_units.UpdateView.as_view(),
        name='edit'),
    path('<int:pk>/delete',
         weight_units.DeleteView.as_view(),
         name='delete'),
]

patterns_fitbit = [
    path('auth', fitbit_client.fitbit_authorize, name='fitbit_auth'),
    path('token', fitbit_client.fitbit_get_token, name='fitbit_token'),
    path('weight', fitbit_client.fitbit_get_weight, name='fitbit_weight'),

]
#
# Actual patterns
#
urlpatterns = [

    # The landing page
    path('',
         misc.index,
         name='index'),

    # The dashboard
    path('dashboard',
         misc.dashboard,
         name='dashboard'),

    # Others
    path('about',
         TemplateView.as_view(template_name="misc/about.html"),
         name='about'),
    path('contact',
         misc.ContactClassView.as_view(template_name="misc/contact.html"),
         name='contact'),
    path('feedback',
         misc.FeedbackClass.as_view(),
         name='feedback'),

    path('language/',
         include((patterns_language, "core"), namespace="language")),
    path('user/', include((patterns_user, "core"), namespace="user")),
    path('license/',
         include((patterns_license, "core"), namespace="license")),
    path('repetition-unit/', include((patterns_repetition_units,
                                      "core"), namespace="repetition-unit")),
    path('weight-unit/',
         include((patterns_weight_units, "core"), namespace="weight-unit")),
    path('fitbit/', include((patterns_fitbit, "core"), namespace='fitbit')),


]
