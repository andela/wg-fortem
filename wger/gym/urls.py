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


from django.urls import (
    path,
    include
)

from wger.gym.views import (
    gym,
    config,
    admin_config,
    user_config,
    admin_notes,
    document,
    contract,
    contract_type,
    contract_option,
    export
)

app_name = "gym"
# 'sub patterns' for gyms
patterns_gym = [
    path(r'list',
        gym.GymListView.as_view(),
        name='list'),
    path(r'new-user-data/view',
        gym.gym_new_user_info,
        name='new-user-data'),
    path(r'new-user-data/export',
        gym.gym_new_user_info_export,
        name='new-user-data-export'),
    path(r'<pk>/members',
        gym.GymUserListView.as_view(),
        name='user-list'),
    path(r'<gym_pk>/add-member',
        gym.GymAddUserView.as_view(),
        name='add-user'),
    path(r'add',
        gym.GymAddView.as_view(),
        name='add'),
    path(r'<pk>/edit',
        gym.GymUpdateView.as_view(),
        name='edit'),
    path(r'<pk>/delete',
        gym.GymDeleteView.as_view(),
        name='delete'),
    path(r'user/<user_pk>/permission-edit',
        gym.gym_permissions_user_edit,
        name='edit-user-permission'),
    path(r'user/<user_pk>/reset-user-password',
        gym.reset_user_password,
        name='reset-user-password'),
]

# 'sub patterns' for gym config
patterns_gymconfig = [
    path(r'<pk>/edit',
        config.GymConfigUpdateView.as_view(),
        name='edit'),
]


# 'sub patterns' for gym admin config
patterns_adminconfig = [
    path(r'<pk>/edit',
        admin_config.ConfigUpdateView.as_view(),
        name='edit'),
]

# 'sub patterns' for gym user config
patterns_userconfig = [
    path(r'<pk>/edit',
        user_config.ConfigUpdateView.as_view(),
        name='edit'),
]

# 'sub patterns' for admin notes
patterns_admin_notes = [
    path(r'list/user/<user_pk>',
        admin_notes.ListView.as_view(),
        name='list'),
    path(r'add/user/<user_pk>',
        admin_notes.AddView.as_view(),
        name='add'),
    path(r'<pk>/edit',
        admin_notes.UpdateView.as_view(),
        name='edit'),
    path(r'<pk>/delete',
        admin_notes.DeleteView.as_view(),
        name='delete'),
]

# 'sub patterns' for user documents
patterns_documents = [
    path(r'list/user/<user_pk>',
        document.ListView.as_view(),
        name='list'),
    path(r'add/user/<user_pk>',
        document.AddView.as_view(),
        name='add'),
    path(r'<pk>/edit',
        document.UpdateView.as_view(),
        name='edit'),
    path(r'<pk>/delete',
        document.DeleteView.as_view(),
        name='delete'),
]

# sub patterns for contracts
patterns_contracts = [
    path(r'add/<user_pk>',
        contract.AddView.as_view(),
        name='add'),
    path(r'view/<pk>',
        contract.DetailView.as_view(),
        name='view'),
    path(r'edit/<pk>',
        contract.UpdateView.as_view(),
        name='edit'),
    path(r'list/<user_pk>',
        contract.ListView.as_view(),
        name='list'),
]

# sub patterns for contract types
patterns_contract_types = [
    path(r'add/<gym_pk>',
        contract_type.AddView.as_view(),
        name='add'),
    path(r'edit/<pk>',
        contract_type.UpdateView.as_view(),
        name='edit'),
    path(r'delete/<pk>',
        contract_type.DeleteView.as_view(),
        name='delete'),
    path(r'list/<gym_pk>',
        contract_type.ListView.as_view(),
        name='list'),
]

# sub patterns for contract options
patterns_contract_options = [
    path(r'add/<gym_pk>',
        contract_option.AddView.as_view(),
        name='add'),
    path(r'edit/<pk>',
        contract_option.UpdateView.as_view(),
        name='edit'),
    path(r'delete/<pk>',
        contract_option.DeleteView.as_view(),
        name='delete'),
    path(r'list/<gym_pk>',
        contract_option.ListView.as_view(),
        name='list'),
]

# sub patterns for exports
patterns_export = [
    path(r'users/<gym_pk>',
        export.users,
        name='users'),
]

#
# All patterns for this app
#

urlpatterns = [
    path(r'', include((patterns_gym, "gym"), namespace="gym")),
    path(r'config/', include((patterns_gymconfig, "config"), namespace="config")),
    path(r'admin-config/', include((patterns_adminconfig, "admin_config"), namespace="admin_config")),
    path(r'user-config/', include((patterns_userconfig, "user_config"), namespace="user_config")),
    path(r'notes/', include((patterns_admin_notes, "admin_note"), namespace="admin_note")),
    path(r'document/', include((patterns_documents, "document"), namespace="document")),
    path(r'contract/', include((patterns_contracts, "contract"), namespace="contract")),
    path(r'contract-type/', include((patterns_contract_types, "contract_type"), namespace="contract_type")),
    path(r'contract-option/', include((patterns_contract_options,
                                       "contract-option"), namespace="contract-option")),
    path(r'export/', include((patterns_export, "export"), namespace="export")),
]
