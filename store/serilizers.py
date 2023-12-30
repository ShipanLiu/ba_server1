from rest_framework import serializers
from .models import Customer, AiModel, Project, Image, ResultSet
from django.db import transaction
from core.serializers import UserSerializer, DetailUserSerializer


# SLizer for AI
class AisModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = AiModel
        fields = ["id", "name", "description"]



class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "project_id", "name", "old_name", "type", "image_url", "created_at", "updated_at"]

    project_id = serializers.IntegerField()
    image_url = serializers.SerializerMethodField()
    # image_local_path = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image_url()

    # def get_image_local_path(self, obj):
    #     return obj.image_local_path()



# class SimpleImageModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ["id", "project_id", "name", "old_name", "type", "image_url", "image_file", "created_at", "updated_at"]
#
#     project_id = serializers.IntegerField()
#     image_url = serializers.SerializerMethodField()
#
#     def get_image_url(self, obj):
#         return obj.image_url()




class ProjectsModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "ai_model_id", "customer_id", "customer_username", "status", "images_nr", "images", "created_at", "updated_at"]

    ai_model_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    customer_username = serializers.SerializerMethodField(read_only=True)
    images = ImageModelSerializer(many=True, read_only=True)
    images_nr = serializers.IntegerField(read_only=True)

    def get_customer_username(self, project:Project):
        return project.customer.user.username



# for creating a project
class CreateProjectsModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "ai_model_id"]

    ai_model_id = serializers.IntegerField()

    def create(self, validated_data):
        # get the customer_id
        customer_id = self.context.get("customer_id")
        # create the project
        project = Project.objects.create(customer_id=customer_id, **validated_data)
        # to return the full project info, create a sLizer
        return project


# for deleting a project
class UpdateProjectsModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']





# Customized SLizer for Customer
class CustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "phone", "birth_date", "user_id", "user"]

    user_id = serializers.IntegerField
    user = DetailUserSerializer(read_only=True)

class PatchCustomerModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["phone", "birth_date"]
