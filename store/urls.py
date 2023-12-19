from django.urls import path, include
# from package drf-nested-routers for building nested router
from rest_framework_nested import routers

from . import views

# initialize the router, create a router instance
router = routers.DefaultRouter()

# register "customer/" endpoints
router.register("customers", views.CustomerViewSet, basename="customers")

urlpatterns = [
    path(r"", include(router.urls)),
]
