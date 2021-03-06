# Generated by Django 2.2.1 on 2019-05-29 07:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(600)], verbose_name='Weight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Weight entry',
                'ordering': ['date'],
                'get_latest_by': 'date',
                'unique_together': {('date', 'user')},
            },
        ),
    ]
