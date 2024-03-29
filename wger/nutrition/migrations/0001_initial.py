# Generated by Django 2.2.1 on 2019-05-31 12:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import wger.utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_author', models.CharField(blank=True, help_text='If you are not the author, enter the name or source here. This is needed for some licenses e.g. the CC-BY-SA.', max_length=50, null=True, verbose_name='Author')),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Accepted'), ('3', 'Declined'), ('4', 'Submitted by administrator'), ('5', 'System ingredient')], default='1', editable=False, max_length=2)),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Date')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('energy', models.IntegerField(help_text='In kcal per 100g', verbose_name='Energy')),
                ('protein', models.DecimalField(decimal_places=3, help_text='In g per 100g of product', max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Protein')),
                ('carbohydrates', models.DecimalField(decimal_places=3, help_text='In g per 100g of product', max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Carbohydrates')),
                ('carbohydrates_sugar', models.DecimalField(blank=True, decimal_places=3, help_text='In g per 100g of product', max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Sugar content in carbohydrates')),
                ('fat', models.DecimalField(decimal_places=3, help_text='In g per 100g of product', max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Fat')),
                ('fat_saturated', models.DecimalField(blank=True, decimal_places=3, help_text='In g per 100g of product', max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Saturated fat content in fats')),
                ('fibres', models.DecimalField(blank=True, decimal_places=3, help_text='In g per 100g of product', max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Fibres')),
                ('sodium', models.DecimalField(blank=True, decimal_places=3, help_text='In g per 100g of product', max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Sodium')),
                ('language', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Language')),
                ('license', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core.License', verbose_name='License')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientWeightUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gram', models.IntegerField(verbose_name='Amount in grams')),
                ('amount', models.DecimalField(decimal_places=2, default=1, help_text='Unit amount, e.g. "1 Cup" or "1/2 spoon"', max_digits=5, verbose_name='Amount')),
                ('ingredient', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='nutrition.Ingredient', verbose_name='Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, editable=False, verbose_name='Order')),
                ('time', wger.utils.fields.Html5TimeField(blank=True, null=True, verbose_name='Time (approx)')),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.CreateModel(
            name='WeightUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('language', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Language')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='NutritionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('description', models.TextField(blank=True, help_text='A description of the goal of the plan, e.g. "Gain mass" or "Prepare for summer"', max_length=2000, verbose_name='Description')),
                ('has_goal_calories', models.BooleanField(default=False, help_text='Tick the box if you want to mark this plan as having a goal amount of calories. You can use the calculator or enter the value yourself.', verbose_name='Use daily calories')),
                ('language', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Language')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='MealItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, editable=False, verbose_name='Order')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='Amount')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrition.Ingredient', verbose_name='Ingredient')),
                ('meal', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='nutrition.Meal', verbose_name='Nutrition plan')),
                ('weight_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nutrition.IngredientWeightUnit', verbose_name='Weight unit')),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='plan',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='nutrition.NutritionPlan', verbose_name='Nutrition plan'),
        ),
        migrations.AddField(
            model_name='ingredientweightunit',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrition.WeightUnit', verbose_name='Weight unit'),
        ),
    ]
