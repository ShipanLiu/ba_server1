"""
for the celery tasks

"""

# tasks.py
from celery import shared_task
from .utility.ai_utils import prepare_cfg, run_ai_model
from .models import Image, ResultSet
from django.conf import settings
import os
import json




@shared_task
def process_image(project_id, image_id, ai_model_id):
    # Retrieve the image instance
    image = Image.objects.get(id=image_id)
    image_name = image.name  # the image_name here is with extensions
    image_old_name = image.old_name
    image_file_path = image.image_url()
    image_base_name = os.path.splitext(image_name)[0]

    cfg_file_path = prepare_cfg(project_id, image_name, ai_model_id)
    # the ai result will be a boolean, True
    ai_processing_successful = run_ai_model(cfg_file_path)

    # Ergebnis-Dictionary vorbereiten
    result_data = {
        "image_id": image_id,
        "image_info": {
            "name": image_name,
            "old_name": image_old_name,
            "image_url": image_file_path
        },
        "success": ai_processing_successful,
        "error_msg": ""
    }

    if ai_processing_successful:
        base_output_path_relative = os.path.join('outputs', f'project_{project_id}', image_base_name)
        detection_image_relative_path = os.path.join(base_output_path_relative, 'text_detection', 'final', 'visual', image_name)
        recognition_image_relative_path = os.path.join(base_output_path_relative, 'text_recognition', 'final', 'visual', image_name)
        interpretation_image_relative_path = os.path.join(base_output_path_relative, 'text_interpretation', 'final', 'visual', image_name)
        # Construct paths for the processed JSON results
        base_output_path = os.path.join(settings.MEDIA_ROOT, 'outputs', f'project_{project_id}', image_base_name)
        # Load JSON results
        detection_json_path = os.path.join(base_output_path, 'text_detection', 'final', 'results.json')
        recognition_json_path = os.path.join(base_output_path, 'text_recognition', 'final', 'results.json')
        interpretation_json_path = os.path.join(base_output_path, 'text_interpretation', 'final', 'floor.json')

        # Check if all 3 JSON files exist, if all exists then means the processing is done[actually if the interpretation_json_path exists, then it means it is done]
        if os.path.exists(detection_json_path) and os.path.exists(recognition_json_path) and os.path.exists(interpretation_json_path):
            with open(detection_json_path, 'r') as file:
                detection_result = json.load(file)
            with open(recognition_json_path, 'r') as file:
                recognition_result = json.load(file)
            with open(interpretation_json_path, 'r') as file:
                interpretation_result = json.load(file)

            # check if the result with the image_id already exists or not, if yes, then update the old tuple:

            result_set, created = ResultSet.objects.update_or_create(
                image_id=image_id,
                defaults={
                    "project_id": project_id,
                    "ai_model_id": ai_model_id,
                    "result_detection": detection_result,
                    "result_recognition": recognition_result,
                    "result_interpretation": interpretation_result,
                    "text_detection_image_path": detection_image_relative_path,
                    "text_recognition_image_path": recognition_image_relative_path,
                    "text_interpretation_image_path": interpretation_image_relative_path,
                }
            )

        else:
            result_data["error_msg"] = f"The singe processing succeeds for image with name: {image_name}, in project with project id: {project_id}, but not all 3 json files are produced"
            result_data["success"] = False
    else:
        result_data["error_msg"] = f"The singe processing failed for image with name: {image_name}, in project with project id: {project_id}"
        result_data["success"] = False

    return result_data