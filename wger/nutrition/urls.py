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

from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import (
    url,
    include,
)

from wger.nutrition.views import (
    ingredient,
    bmi,
    calculator,
    plan,
    meal,
    meal_item,
    unit,
    unit_ingredient
)

app_name = "nutrition"
# sub patterns for nutritional plans
patterns_plan = [
    path('overview/',
         plan.overview,
         name='overview'),
    path('add/',
         plan.add,
         name='add'),
    path('<id>/view/',
         plan.view,
         name='view'),
    path('<pk>/copy/',
         plan.copy,
         name='copy'),
    path('<pk>/delete/',
         login_required(plan.PlanDeleteView.as_view()),
         name='delete'),
    path('<pk>/edit/',
         login_required(plan.PlanEditView.as_view()),
         name='edit'),
    url(r'^(?P<id>\d+)/pdf/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        plan.export_pdf,
        name='export-pdf'),
    path('<id>/pdf/',
         plan.export_pdf,
         name='export-pdf'),
]


# sub patterns for meals
patterns_meal = [
    path('<plan_pk>/meal/add/',
         login_required(meal.MealCreateView.as_view()),
         name='add'),
    path('<pk>/edit/',
         login_required(meal.MealEditView.as_view()),
         name='edit'),
    path('<id>/delete/',
         meal.delete_meal,
         name='delete'),
]


# sub patterns for meal items
patterns_meal_item = [
    path('<meal_id>/item/add/',
         login_required(meal_item.MealItemCreateView.as_view()),
         name='add'),
    path('<pk>/edit/',
         login_required(meal_item.MealItemEditView.as_view()),
         name='edit'),
    path('<item_id>/delete/',
         meal_item.delete_meal_item,
         name='delete'),
]


# sub patterns for ingredient
patterns_ingredient = [
    path('<pk>/delete/',
         ingredient.IngredientDeleteView.as_view(),
         name='delete'),
    path('<pk>/edit/',
         ingredient.IngredientEditView.as_view(),
         name='edit'),
    path('add/',
         login_required(ingredient.IngredientCreateView.as_view()),
         name='add'),
    path('overview/',
         ingredient.IngredientListView.as_view(),
         name='list'),
    path('pending/',
         ingredient.PendingIngredientListView.as_view(),
         name='pending'),
    path('<pk>/accept/',
         ingredient.accept,
         name='accept'),
    path('<pk>/decline/',
         ingredient.decline,
         name='decline'),
    path('<id>/view/',
         ingredient.view,
         name='view'),
    path('<id>/view/<slug>/',
        ingredient.view,
        name='view'),
]


# sub patterns for weight units
patterns_weight_unit = [
    path('list/',
         unit.WeightUnitListView.as_view(),
         name='list'),
    path('add/',
         unit.WeightUnitCreateView.as_view(),
         name='add'),
    path('<pk>/delete/',
         unit.WeightUnitDeleteView.as_view(),
         name='delete'),
    path('<pk>/edit/',
         unit.WeightUnitUpdateView.as_view(),
         name='edit'),
]


# sub patterns for weight units / ingredient cross table
patterns_unit_ingredient = [
    path('add/<ingredient_pk>/',
         unit_ingredient.WeightUnitIngredientCreateView.as_view(),
         name='add'),
    path('<pk>/edit/',
         unit_ingredient.WeightUnitIngredientUpdateView.as_view(),
         name='edit'),
    path('<pk>/delete/',
         unit_ingredient.WeightUnitIngredientDeleteView.as_view(),
         name='delete'),
]


# sub patterns for BMI calculator
patterns_bmi = [
    path('',
         bmi.view,
         name='view'),
    path('calculate',
         bmi.calculate,
         name='calculate'),
    path('chart-data',
         bmi.chart_data,
         name='chart-data'),  # JS
]


# sub patterns for calories calculator
patterns_calories = [
    path('',
         calculator.view,
         name='view'),
    path('bmr',
         calculator.calculate_bmr,
         name='bmr'),
    path('activities',
         calculator.calculate_activities,
         name='activities'),  # JS
]

urlpatterns = [
    path('', include((patterns_plan, "nutrition"), namespace="plan")),
    path('meal/', include((patterns_meal, "nutrition"), namespace="meal")),
    path('meal/item/', include((patterns_meal_item, "nutrition"),
                               namespace="meal_item")),
    path('ingredient/', include((patterns_ingredient, "nutrition"),
                                namespace="ingredient")),
    path('unit/', include((patterns_weight_unit, "nutrition"),
                          namespace="weight_unit")),
    path('unit-to-ingredient/', include((patterns_unit_ingredient,
                                         "nutrition"),
                                        namespace="unit_ingredient")),
    path('calculator/bmi/',
         include((patterns_bmi, "nutrition"), namespace="bmi")),
    path('calculator/calories/', include((patterns_calories, "nutrition"),
                                         namespace="calories")),
]
