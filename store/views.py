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
from rest_framework.parsers import MultiPartParser, FormParser

# for customize the Viewset(replacing the ModelViewSet)
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin, UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet

# inside
from .models import Customer, AiModel, Project, Image, ResultSet
from .serilizers import (CustomerModelSerializer, PutCustomerModelSerilizer,
                         AisModelSerilizer, ProjectsModelSerilizer,
                         CreateProjectsModelSerilizer, UpdateProjectsModelSerilizer,
                         ImageModelSerializer)
from .permissions import IsAdminOrReadOnly


# supports GET-List
# supports POST-List(set permissions: IsAdminOrReadOnly, only stuffed admin can add ai-models, others can only view)
# supports GET-Detail
class AIsViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    # queryset
    queryset = AiModel.objects.all()
    # serilizer classs
    serializer_class = AisModelSerilizer
    # set permissions
    permission_classes = [IsAdminOrReadOnly]

    # pass context to slizer
    def get_serializer_context(self):
        return {
            "request": self.request
        }

# supports GET-List -> /store/projects
# supports POST-List -> /store/projects
# supports GET-Detail -> /store/projects/1
# supports PATCH-Detail -> /store/projects/1
# supports DELETE-Detail -> /store/projects/1
# grand all permissions for al while developing
class ProjectsViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # queryset
    def get_queryset(self):
        return Project.objects.annotate(images_nr=Count("images")).prefetch_related("images").all()
    # serilizer classs
    def get_serializer_class(self):
        if self.action == "create":
            return CreateProjectsModelSerilizer
        # "partial_update" is for patch
        elif self.action == "partial_update":
            return UpdateProjectsModelSerilizer
        else:
            return ProjectsModelSerilizer

    # pass context to slizer
    def get_serializer_context(self):
        return {
            "request": self.request
        }



    @action(detail=True, methods=["GET"], url_path='images')
    def images(self, request, pk=None):

        project = self.get_object()

        # get queryset
        target_queryset = Image.objects.filter(project=project)
        # create slizer based on the Database instance
        sLizer = ImageModelSerializer(target_queryset, many=True)
        # change the customer to JSON
        return Response(sLizer.data)


    # "detail=True" means "/store/projects/1/images-upload" not "/store/projects/images-upload"
    @action(detail=True, methods=["POST"], url_path='images-upload', parser_classes=[MultiPartParser, FormParser])
    def images_upload(self, request, pk=None):

        project = self.get_object()

        """
        Uploads images to a specific project.
        Suppose you have an HTML form with an input like <input type="file" name="images" multiple>.
        The user selects multiple files to upload.
        The request body would contain each of these files under the 'images' key.
        """

        # "images" should be teh form name in frontend
        images_data = request.FILES.getlist('images')
        print(images_data)
        images = []  # List to store the created image instances
        for index, image_data in enumerate(images_data, start=1):
            # Construct the image name using project ID and loop index, for example p1_1.png,  p1_2.png ...
            image_name = f"p{project.id}_{index}"
            image_type = image_data.name.split(".")[-1]
            print(image_name)
            image = Image.objects.create(project_id=project.id, name=image_name, image_file=image_data, type=image_type)
            images.append(image)

        # Serialize the list of created image instances
        serializer = ImageModelSerializer(images, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(detail=True, methods=['post'], url_path='upload-images', parser_classes=[MultiPartParser, FormParser])
    # def upload_images(self, request, pk=None):
    #     project = self.get_object()
    #     images_data = request.FILES.getlist('images')
    #
    #     images = []  # List to store the created image instances
    #     for index, image_data in enumerate(images_data, start=1):
    #         image_name = f"p{project.id}_{index}.{image_data.name.split('.')[-1]}"
    #         image = Image.objects.create(project=project, name=image_name, image_file=image_data)
    #         images.append(image)
    #
    #     # Serialize the list of created image instances
    #     serializer = ImageModelSerializer(images, many=True)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# supports GET-List -> /store/images
# supports POST-List -> /store/images
# supports GET-Detail -> assocated with project
# supports DELETE-Detail -> assocated with project
# grand all permissions for al while developing
class ImagesViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    pass



# supports GET-List -> /store/project/project_pk/results
# grand all permissions for al while developing
class ResultsViewSet(ModelViewSet):
    pass












# ViewSet for Customer
class BaseCustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    pass


# ViewSet for Customer
# support : create / retrieve / update a customer
# no support; get customer list
class CustomerViewSet(BaseCustomerViewSet):
    # queryset
    def get_queryset(self):
        return Customer.objects.all()
    # serilizer
    serializer_class = CustomerModelSerializer

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
            sLizer = CustomerModelSerializer(customer)
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






