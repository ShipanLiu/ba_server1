# Bachelor Project 🎓

## Project Title:
**Conceptualization and Implementation of a Web Application (Backend) for Processing Technical Drawings**

## About 📖:
This project offers a comprehensive solution for processing technical drawings. The workflow includes:

- 🧑‍💼 **User Management:** Create and authenticate users.
- 🔑 **Secure Authentication:** Ensures secure access with token-based authentication.
- 📋 **Project Management:** Organize and manage your technical drawing projects.
- 🖼️ **Image Uploading:** Upload technical drawings for processing.
- 🤖 **AI Processing:** Utilize AI models to analyze and process drawings.
- 📈 **Result Retrieval:** Access and review the processed results.
- 🚀 **User-Friendly API:** A well-documented and easy-to-use backend API.

The project aims to streamline the processing of technical drawings.


## 🚀 Getting Started
This guide will walk you through setting up the project and getting it up and running on your local machine. It also includes steps to utilize its features for processing technical drawings.

### 📋 Prerequisites
Before you begin, make sure you have Python 3.10.13 installed on your system. All required dependencies for this project are listed in `full_requirements.txt`.

### 🛠️ Setting Up the Project
Follow these steps to set up the project:

1. **Clone the Repository:**
   Clone this project to your local machine.

2. **Install Dependencies:**
   Navigate to the project directory and install the required dependencies:
   ```bash
   pip install -r full_requirements.txt
   
3. **Setup Database:** Install MySQL on your machine and create a secrets.py file in the project root with the following content, put the secrets.py under /project folder
   ```text
   # secrets.py (add this file to .gitignore)
    DATABASE_NAME = "YOUR_DATABASE_NAME"
    DATABASE_USER = "USER"
    DATABASE_PASSWORD = "USER_PWD"
    DATABASE_HOST = "YOUR_HOST"
    DATABASE_PORT = "3306"  # Default port for MySQL

4. **Do Initial Migrations** Run the following commands to initialize the database tables:
    ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Download ai weight file** Download the AI model weights from this https://drive.google.com/file/d/1bSP7DinU-4ZfdZFVOZf6zPM8tG7KMvGQ/view?usp=sharing. Unzip model_weights.zip and place its contents in the /store/ai directory.

6. **Start Project** Run the Django development server:
    ```bash
   python manage.py runserver
   
7. **Create Superuser** Create a superuser to access the Django admin panel:
    ```bash
   # create superuser/admin
    python manage.py createsuperuser

## 📘 User Behavior Guide

### Step 1: User Creation and Authentication 🙋‍♂️
1. Register: Visit http://127.0.0.1:8001/auth/users/ to create a user.
2. Login: Visit http://127.0.0.1:8001/auth/jwt/create to log in and obtain an access-token. Include this token in all subsequent requests.
3. Profile: Visit http://127.0.0.1:8001/store/customers/me/ to view and update your information (birth_date and phone) using the PATCH method.
4. AI Models: Visit http://127.0.0.1:8001/store/ais/ to browse available AI models.
5. Projects: Visit http://127.0.0.1:8001/store/projects/ to view and create projects, like creating one with `project_id = 19`.
6. **Next Step:** Move on to Step 2.

### Step 2: Uploading Images to a Project 🖼️
1. After creating projects, visit http://127.0.0.1:8001/store/projects/ to see your projects. Example data is in [`all_projects.json`](/steps_example_project_19/step2_project_create_view_upload_images/all_projects.json) at `/steps_example_project_19/step2_project_create_view_upload_images`.
2. Image Upload: For project 19, upload images at http://127.0.0.1:8001/store/projects/19/images.
3. View Project: Then, visit http://127.0.0.1:8001/store/projects/19/ for details of project 19. Find [`project_19.json`](/steps_example_project_19/step2_project_create_view_upload_images/project_19.json) in the same folder.
4. **Next Step:** Head to Step 3.

### Step 3: Triggering AI Processing ⚙️
1. Trigger: With images in project 19, start processing by POSTing to http://127.0.0.1:8001/store/projects/19/start/.
2. Processing Time: It takes around 40 seconds, approximately 20 seconds per image.
3. Results: Check [`trigger_response.json`](/steps_example_project_19/step3_trigger/trigger_response.json) in `/steps_example_project_19/step3_trigger/`.
4. **Next Step:** Proceed to Step 4.

### Step 4: Accessing the Result Set 📈
1. Result List: Access all results for project 19 at http://127.0.0.1:8001/store/projects/19/results/.
2. Specific Results: For results of image ID 55, visit http://127.0.0.1:8001/store/projects/19/results/55.
3. Download: [`project_19_results.json`](/steps_example_project_19/step4_get_result_set/project_19_results.json) is available in the `/steps_example_project_19/step4_get_result_set/` directory.
4. **Next Step:** Continue to Step 5.

### Step 5: Updating AI Model and Recreating Results 🔄
1. Update AI Model: Change the AI model of project 19 by PATCHing to http://127.0.0.1:8001/store/projects/19/ with a new `ai_model_id`.
2. Redo Steps: Repeat Steps 3 and 4 to process the images with the new AI model and retrieve the updated results.


## 🛠️ Used Frameworks/Packages

- **[Django](https://www.djangoproject.com/):** A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **[django-filter](https://django-filter.readthedocs.io/en/stable/):** A reusable application for Django, providing a way to filter querysets dynamically.
- **[django-templated-mail](https://github.com/sunscrapers/django-templated-mail):** Django email backend with template-based emails.
- **[Django REST framework](https://www.django-rest-framework.org/):** A powerful and flexible toolkit for building Web APIs.
- **[djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/):** A JSON Web Token authentication plugin for Django REST Framework.
- **[Djoser](https://djoser.readthedocs.io/en/latest/):** REST implementation of Django authentication system.
- **[drf-nested-routers](https://github.com/alanjds/drf-nested-routers):** An extension for Django REST Framework's routers for working with nested resources.
- **[Pillow](https://pillow.readthedocs.io/en/stable/):** The Python Imaging Library adds image processing capabilities to your Python interpreter.

For a complete list of dependencies, refer to [`full_requirements.txt`](/full_requirements.txt) in the project directory.
