import os

def project_image_directory_path(instance, filename):
    # The directory name will be based on the project's ID
    project_directory = f'project_{instance.project.id}'

    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]  # Extracts file extension

    # project1/p1_uuid.png
    return os.path.join(project_directory, f"{instance.name}.{ext}")


# def project_result_image_directory_path(instance, filename):
#     # Directory based on the project's ID
#     project_directory = f'outputs/project_{instance.project.id}'
#
#     # Rename file based on the type of result
#     # Use the instance's class name or a specific attribute to determine the file name
#     if isinstance(instance, DetectionResult):
#         new_filename = 'detection_image'
#     elif isinstance(instance, RecognitionResult):
#         new_filename = 'recognition_image'
#     elif isinstance(instance, InterpretationResult):
#         new_filename = 'interpretation_image'
#     else:
#         # Default case, or raise an error if appropriate
#         new_filename = 'result'
#
#     # Add a UUID to ensure the filename is unique
#     file_uuid = uuid.uuid4()
#     ext = filename.split('.')[-1]  # Extracts file extension
#
#     return os.path.join(project_directory, f"{file_uuid}_{new_filename}.{ext}")