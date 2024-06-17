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

   after migration, you need to insert to the ai model table with 2 records:
   [
    {
        "id": 1,
        "name": "ai_best",
        "description": "best"
    },
    {
        "id": 2,
        "name": "ai_epoch_299",
        "description": "epoch_299"
    }
   ]


5. **Download ai weight file** Download the AI model weights from this https://drive.google.com/file/d/1bSP7DinU-4ZfdZFVOZf6zPM8tG7KMvGQ/view?usp=sharing. Unzip model_weights.zip and place its contents in the /store/ai directory.

6. **Start Project** Run the Django development server:
    ```bash
   python manage.py runserver
   
7. **Create Superuser** Create a superuser to access the Django admin panel under /admin:
    ```bash
   # create superuser/admin
    python manage.py createsuperuser

## 📘 User Behavior Guide

### Step 1: User Creation and Authentication 🙋️
#### 1. Register: Visit `/auth/users/` to create a user.
![Alt text](screenshots/apis/customers/01_user_create.png)
#### 2. Login: Visit `/auth/jwt/create` to log in and obtain an access-token. Include this token in all subsequent requests.
##### Get access-token
![Alt text](screenshots/apis/customers/gifs/01_get_access_token.gif)
##### Set up access-token
![Alt text](screenshots/apis/customers/03_1_set_access_token.png)
#### 3. Refresh: Visit `/auth/jwt/refresh` to get a new access-token if the current access-token is expired.
![Alt text](screenshots/apis/customers/gifs/03_refresh_token.gif)
#### 4. Profile: Visit `/store/customers/me/` to view and update your information (birth_date and phone) using the PATCH method.
##### View customer information
![Alt text](screenshots/apis/customers/03_2_get_me_info.png)
##### Update customer information
![Alt text](screenshots/apis/customers/gifs/02_change_me.gif)
#### 5. AI Models: Visit `/store/ais/` to browse available AI models.
![Alt text](screenshots/apis/ais/01_get_ais.png)

### Step 2: Project 🖼️
#### 1. Create projects: Visit `/store/projects/` to create projects.
![Alt text](screenshots/apis/projects/01_create_projects.png)
#### 2. After creating projects, visit `/store/projects/` again to see your projects update . Example data is in [`all_projects.json`](/steps_example_project_19/step2_project_create_view_upload_images/all_projects.json).
![Alt text](screenshots/apis/projects/02_view_projects.png)
#### 3. You can view a singe project:
![Alt text](screenshots/apis/projects/03_single_view.png)
#### 4. You can modify details of a single project:
![Alt text](screenshots/apis/projects/04_modify_single.png)
#### 5. You can delete a single project:
##### Succeed
![Alt text](screenshots/apis/projects/05_delate_success.png)
##### Failed
![Alt text](screenshots/apis/projects/06_delete_failed.png)



### Step 3: Image 🏙️
#### 1. Uploading images to a project
![Alt text](screenshots/apis/images/01_upload_images.png)
#### 2. Retrieving image list of a project
![Alt text](screenshots/apis/images/02_get_image_list.png)
#### 3. Getting a specific image of a project
![Alt text](screenshots/apis/images/03_get_single_image.png)
#### 4. Deleting a specific image of a project
![Alt text](screenshots/apis/images/04_delete_a_image.png)



### Step 4: Triggering AI Processing ⚙️
#### 1. Triggerring: With images uploaded to project 22, start processing
##### This is a long request, response will be returned after finishing processing
![Alt text](screenshots/apis/triggering/01_1_triggering_start.png)
##### The response results
![Alt text](screenshots/apis/triggering/01_2_triggering_finished.png)
#### 2. Uploading a new image(image5) 
![Alt text](screenshots/apis/triggering/02_new_image.png)
#### 3. Start processing the unprocessed images(here image5)in this project
![Alt text](screenshots/apis/triggering/03_start_rest.png)
#### 4. Check this updated project again
![Alt text](screenshots/apis/triggering/04_updated_project.png)
#### 5. Example Results: Check [`trigger_response.json`](/steps_example_project_19/step3_trigger/trigger_response.json)


### Step 5: Accessing the Result Set 📈
#### 1. Result List
![Alt text](screenshots/apis/resultsets/01_resultset_list.png)
#### 2. Result of a specific image of the project 
![Alt text](screenshots/apis/resultsets/02_resultset_single.png)
#### 3. Example Results Set: [`project_19_resultset.json`](/steps_example_project_19/step4_get_result_set/project_19_resultset.json)



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
