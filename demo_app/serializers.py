from rest_framework import serializers
# import models
from demo_app.models import (PersonOne,
                             PersonTwo,
                             CabinetOne,
                             CabinetTwo
                             )


class PersonOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonOne
        fields = ['id', 'first_name', 'last_name', 'phone_number', ]
        depth = 0


class PersonTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonTwo
        fields = ['id', 'fname', 'lname', 'phone', ]
        depth = 0


class CabinetOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinetOne
        fields = ['id', 'name', 'location', ]
        depth = 0


class CabinetTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinetTwo
        fields = ['id', 'cab_name', 'room', ]
        depth = 0
