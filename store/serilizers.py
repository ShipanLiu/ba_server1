from rest_framework import serializers
from .models import Customer, AiModel, Project, Image, ResultSet


# SLizer for AI
class AisModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = AiModel
        fields = ["id", "name", "description"]



class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "name", "project_id", "image_file", "type", "created_at", "updated_at"]

    project_id = serializers.IntegerField()



class SimpleImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "name", "type", "created_at", "updated_at"]




class ProjectsModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "ai_model_id", "status", "images_nr", "images", "created_at", "updated_at"]

    ai_model_id = serializers.IntegerField()
    images = SimpleImageModelSerializer(many=True, read_only=True)
    images_nr = serializers.IntegerField(read_only=True)


# for creating a project
class CreateProjectsModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "ai_model_id"]

    ai_model_id = serializers.IntegerField()


# for deleting a project
class UpdateProjectsModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']





# Customized SLizer for Customer
class CustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date"]

    user_id = serializers.IntegerField()

class PutCustomerModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date"]

    user_id = serializers.IntegerField(read_only=True)