from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters
from handyhelpers.mixins.viewset_mixins import InvalidLookupMixin

# import models
from demo_app.models import (PersonOne,
                             PersonTwo,
                             CabinetOne,
                             CabinetTwo
                             )

# import serializers
from demo_app.serializers import (PersonOneSerializer,
                                  PersonTwoSerializer,
                                  CabinetOneSerializer,
                                  CabinetTwoSerializer
                                  )


class PersonOneViewSet(InvalidLookupMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows PersonOnes to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = PersonOne
    queryset = model.objects.all().select_related()
    serializer_class = PersonOneSerializer
    filter_fields = ['id', 'first_name', 'last_name', 'phone_number', ]
    search_fields = filter_fields


class PersonTwoViewSet(InvalidLookupMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows PersonTwos to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = PersonTwo
    queryset = model.objects.all().select_related()
    serializer_class = PersonTwoSerializer
    filter_fields = ['id', 'fname', 'lname', 'phone', ]
    search_fields = filter_fields


class CabinetOneViewSet(InvalidLookupMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows CabinetOnes to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = CabinetOne
    queryset = model.objects.all().select_related()
    serializer_class = CabinetOneSerializer
    filter_fields = ['id', 'name', 'location', ]
    search_fields = filter_fields


class CabinetTwoViewSet(InvalidLookupMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows CabinetTwos to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = CabinetTwo
    queryset = model.objects.all().select_related()
    serializer_class = CabinetTwoSerializer
    filter_fields = ['id', 'cab_name', 'room', ]
    search_fields = filter_fields










