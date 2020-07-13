from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from demo_app import apis

app_name = 'demo_app'

router = routers.DefaultRouter()

# demo_app API Endpoints
router.register(r'personone', apis.PersonOneViewSet, 'personone')
router.register(r'persontwo', apis.PersonTwoViewSet, 'persontwo')
router.register(r'cabinetone', apis.CabinetOneViewSet, 'cabinetone')
router.register(r'cabinettwo', apis.CabinetTwoViewSet, 'cabinettwo')


urlpatterns = [

    # API views
    path('api/', include(router.urls)),

]
