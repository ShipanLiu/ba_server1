#django
from django.shortcuts import render
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

# rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# for customize the Viewset(replacing the ModelViewSet)
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin, UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet

# inside
from .models import Customer
from .serilizers import CustomerModalSerializer, PutCustomerModelSerilizer


# ViewSet for Customer
class BaseCustomerViewSet(CreateModelMixin, RetrieveModelMixin,
                          UpdateModelMixin, ListModelMixin,
                          DestroyModelMixin,
                          GenericViewSet):
    pass


# ViewSet for Customer
# support : create / retrieve / update a customer
# no support; get customer list
class CustomerViewSet(BaseCustomerViewSet):
    # queryset
    def get_queryset(self):
        return Customer.objects.all()
    # serilizer
    serializer_class = CustomerModalSerializer

    #define permissions: as a admin, I can modify and check all the Customers
    permission_classes = [IsAdminUser]

    # pas ocntext
    def get_serializer_context(self):
        return {
            "request": self.request
        }
    # create action "me", to access the "me" for getting the current customer use url "http://127.0.0.1:8000/store/customers/me/"
    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        # if user does not even exist, then the request.user = AnonymousUser
        if not request.user.id:
            return Response("you need to login first, and send me request with your access-token", status=status.HTTP_401_UNAUTHORIZED)
        # get the target_cutomer, if not exist, then create(the customer should exist normally)
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            # create sLizer
            sLizer = CustomerModalSerializer(customer)
            # return Slizer.data
            return Response(sLizer.data)
        elif request.method == "PUT":
            # create dSlizer based on the customer
            dSlizer = PutCustomerModelSerilizer(customer, data=request.data)
            # validate data
            dSlizer.is_valid(raise_exception=True)
            # save
            dSlizer.save()
            return Response(dSlizer.data)

