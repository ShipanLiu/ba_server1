from uuid import uuid4
import time
import sys, os, shutil
from celery import group


#django
from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings


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
from .serilizers import (CustomerModelSerializer, PatchCustomerModelSerilizer,
                         AisModelSerilizer, ProjectsModelSerilizer,
                         CreateProjectsModelSerilizer, UpdateProjectsModelSerilizer,
                         ImageModelSerializer)
from .permissions import IsAdminOrReadOnly
from .utility.ai_utils import prepare_cfg, run_ai_model
from .tasks import process_image



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
    @action(detail=False, methods=["GET", "PATCH"], permission_classes=[IsAuthenticated])
    def me(self, request):
        # if user does not even exist, then the request.user = AnonymousUser
        # if you have added the "permission_classes=[IsAuthenticated]", then here is checking "request.user.id" is no needed
        if not request.user.id:
            return Response("you need to login first, and send me request with your access-token", status=status.HTTP_401_UNAUTHORIZED)
        # get the target_cutomer, if not exist, then create(the customer should exist normally)
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            # create sLizer
            sLizer = CustomerModelSerializer(customer)
            # return Slizer.data
            return Response(sLizer.data)
        elif request.method == "PATCH":
            # create dSlizer based on the customer
            dSlizer = PatchCustomerModelSerilizer(customer, data=request.data)
            # validate data
            dSlizer.is_valid(raise_exception=True)
            # save
            dSlizer.save()
            return Response(dSlizer.data)







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
    # the basic permission is to be authenticated(angemeldet),
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # if you are admin/stuffed(inside workers), you are free to check all the
        if user.is_staff:
            return Project.objects.annotate(images_nr=Count("images")).select_related("customer").prefetch_related("images").all()
        # Use get_object_or_404 to get the customer ID or return a 404 response if not found
        # BAD! this violates "command or query principle"
        customer = Customer.objects.only("id").get(user_id=user.id)
        return Project.objects.annotate(images_nr=Count("images")).select_related("customer").prefetch_related("images").filter(customer_id=customer.id)
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
        user = self.request.user
        customer = Customer.objects.get(user_id=user.id)
        return {
            "request": self.request,
            "customer_id": customer.id
        }

    # overwrite the create() for responding a full project structure
    def create(self, request, *args, **kwargs):
        # Create serializer with incoming data
        serializer = CreateProjectsModelSerilizer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        project = serializer.save()

        # Serialize the response with full details
        response_serializer = ProjectsModelSerilizer(project, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    # overwrite the partical_update() and update() for responding a full project structure
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Serialize the response with full details
        response_serializer = ProjectsModelSerilizer(instance)
        return Response(response_serializer.data)

    # "detail=True" means "/store/projects/1/images-upload" not "/store/projects/images-upload"
    @action(detail=True, methods=["POST", "GET"], url_path='images', parser_classes=[MultiPartParser, FormParser])
    def images(self, request, pk=None):

        project = self.get_object()

        if request.method == "GET":
            # get queryset
            target_queryset = Image.objects.filter(project=project)
            # create slizer based on the Database instance
            sLizer = ImageModelSerializer(target_queryset, many=True)
            # change the customer to JSON
            return Response(sLizer.data)

        elif request.method == "POST":
            """
            Uploads images to a specific project.
            Suppose you have an HTML form with an input like <input type="file" name="images" multiple>.
            The user selects multiple files to upload.
            The request body would contain each of these files under the 'images' key.
            """

            # Get the total number of images already uploaded for this project
            existing_images_count = Image.objects.filter(project_id=project.id).count()

            # "images" should be teh form name in frontend
            images_data = request.FILES.getlist('images')

            good_images = []  # List to store the created image instances
            bad_images = []
            # image_index = existing_images_count
            for image_data in images_data:
                # get the extension of image_data
                image_ext = image_data.name.split(".")[-1].lower()
                image_old_name = image_data.name.split(".")[0]
                # we only support 'png' and 'jpg' file
                if image_ext not in ['png', 'jpg']:
                    bad_images.append(image_data.name)
                    continue
                # image_index += 1
                # Construct the image name using project ID and loop index, for example p1_1.png,  p1_2.png ...
                image_name = f"{uuid4()}.{image_ext}"  # in database, the image name is with extension
                image = Image.objects.create(project_id=project.id, name=image_name, old_name=image_old_name, image_file=image_data, type=image_ext)
                good_images.append(image)

            if good_images:
                # Serialize the list of created image instances
                serializer = ImageModelSerializer(good_images, many=True)
                if bad_images:
                    return Response({"data": serializer.data, "error": True, "error_msg": "part of the images are uploaded but some images does not have extensions 'png' or 'jpg',please upload PART again", "bad_images": bad_images}, status=status.HTTP_202_ACCEPTED)
                return Response({"data": serializer.data, "error": False, "error_msg": "", "bad_images": bad_images}, status=status.HTTP_201_CREATED)
            return Response({"data": "", "error": True, "error_msg": "no images have extensions 'png' or 'jpg', please upload ALL again", "bad_images": bad_images}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'DELETE'], url_path='images/(?P<image_id>\d+)')
    def image_detail(self, request, pk=None, image_id=None):
        project = self.get_object()
        image = get_object_or_404(Image, pk=image_id, project_id=project.id)

        if request.method == 'GET':
            serializer = ImageModelSerializer(image)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            image.delete()
            return Response({"message": f"image with id {image_id} is deleted"}, status=status.HTTP_204_NO_CONTENT)


    # this is a trigger endpoints while visiting "http://127.0.0.1:8001/store/projects/1/start"()
    # extract project_id  -->  get image_nr, model_id
    # for a single image, dynamic yaml file is created, and the call the run_ai_model() function
    # implementation for processing the whole images of a project
    # if the procesing is done, then save the 3 images path and the 3 json files into RestltSet model
    @action(detail=True, methods=["POST"], url_path='start')
    def start(self, request, pk=None):
        project = self.get_object()
        project_id = project.id
        ai_model_id = project.ai_model.id
        ai_model_name = project.ai_model.name

        # the related output path
        output_path = os.path.join(settings.MEDIA_ROOT, 'outputs', f'project_{project_id}')

        # for timeing reasons(retriggering will take more time), delete the old output
        if os.path.exists(output_path):
            shutil.rmtree(output_path)

        # start time counting
        start_time = time.time()

        # Create a group of image processing tasks
        task_group = group(process_image.s(project_id, image.id, ai_model_id) for image in project.images.all())

        # Execute the group of tasks and wait for all results synchronously
        result_group = task_group.apply()

        successful_results = []
        failed_results = []
        # Process each result
        for result in result_group.results:
            result_data = result.get()
            if result_data["success"]:
                successful_results.append(result_data)
            else:
                failed_results.append(result_data)

        # end time counting
        end_time = time.time()
        total_processing_time = end_time - start_time


        # Construct the response data
        response_data = {
            "project_id": project_id,
            "ai_model_id": ai_model_id,
            "ai_model_name": ai_model_name,
            "error": len(failed_results) > 0,
            "error_msg": "" if not failed_results else "Errors occurred during processing. Details please see failed key",
            "successful_results": successful_results,
            "failed_results": failed_results,
            "total_processing_time": total_processing_time  # Gesamtverarbeitungszeit hinzufügen
        }

        # Determine the status code based on whether any errors occurred
        status_code = status.HTTP_200_OK if not failed_results else status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response_data, status=status_code)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>ResultSetViewSet>>>>>>>>>>>>>>>>>>







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

















