import os

def project_image_directory_path(instance, filename):
    # The directory name will be based on the project's ID
    project_directory = f'project_{instance.project.id}'

    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]  # Extracts file extension
    # project1/p1_uuid.png
    return os.path.join(project_directory, filename)

