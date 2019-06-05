from rest_framework import serializers

from wger.core.models import User


class GymTrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'is_active',
                  'id')
