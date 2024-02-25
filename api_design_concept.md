# API Design for User Activity

### User Creating
- **Endpoint:** `/auth/users`
- **Method:** POST
- **Request Body (Example):**
  ```json
  {
      "username": "user2",
      "password": "19980223",  // requires passwords to have at least 8 characters/numbers. 
      "email": "user2@email.com",  // each user has a unique email
      "first_name": "UserTwo",
      "last_name": "Liu"
  }
- **Response Body (Example):**
  ```json
  {
    "id": 3,
    "username": "user2",
    "email": "user2@email.com",
    "first_name": "UserTwo",
    "last_name": "Liu"
  }

### User Login
- **Endpoint:** `/auth/jwt/create`
- **Method:** POST
- **Request Body (Example):**
  ```json
  {
      "username": "user2",
      "password": "19980223"
  }
- **Response Body (Example):**
  ```json
  {
      "refresh": "eyJhbGciOiJIUzI1...lUVoIf55uX23Cy6NEb-WyUR2HADfh5gvqBDZvc",
      "access": "eyJhbGciOiJIUzI1N...1355GU3maSBkbw1dYaDkdmeHv32Ipg9pSrfTv_g"
  }

- **Notice:**
  ```text
  After the initial authentication, it's important to include the access token in the request header for any subsequent requests to the server. If the authentication request header isn't set with a valid access token, the user won't be able to access the API. This helps ensure that only authenticated users can interact with the REST API.
  
### Refresh for New Access Token
- **Endpoint:** `/auth/jwt/refresh`
- **Method:** POST
- **Request Body (Example):**
  ```json
  {
      "refresh": "eyJhbGciOiJIUzI1...lUVoIf55uX23Cy6NEb-WyUR2HADfh5gvqBDZvc"
  } 
- **Response Body (Example):**
  ```json
  {
      "access": "eyJhbGciOiJIUzI1Ni...1dYa2EtXiqNABMNSbvG7wjpgBXgHXdEvbVwOk"
  }




[//]: # (Customer)





# API Design for Customer

### Check Customer Profile
- **Endpoint:** `/store/customers/me/`
- **Method:** GET
- **Response Body (Example):**
  ```json
  {
      "id": 6,
      "phone": "",
      "birth_date": "",
      "user_id": 6,
      "user": {
          "username": "jier",
          "email": "jier@email.com",
          "first_name": "Jier",
          "last_name": "Liu"
      }
  }


### Update Customer Profile
- **Endpoint:** `/store/customers/me/`
- **Method:** PATCH
- **Request Body (Example):**
  ```json
  {
      "phone": "000",
      "birth_date": "1990-10-10"
  }
- **Response Body (Example):**
  ```json
  {
      "id": 6,
      "phone": "000",
      "birth_date": "1990-10-10",
      "user_id": 6,
      "user": {
          "username": "jier",
          "email": "jier@email.com",
          "first_name": "Jier",
          "last_name": "Liu"
      }
  }
  



[//]: # (AI)





# API Design for AI Model

### Retrieve all AI models
- **Endpoint:** `/store/ais`
- **Method:** GET
- **Response Body (Example):**
  ```json
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
  





[//]: # (Projects)





# API Design for Project

### Retrieve Project list
- **Endpoint:** `/store/projects`
- **Method:** GET
- **Response Body (Example):**
  ```json
  [
      {
          "id": 14,
          "name": "project3",
          "description": "this is a testing project3 hahaha",
          "ai_model_id": 2,
          "customer_id": 6,
          "customer_username": "jier",
          "status": "COMPLETED",
          "images_nr": 2,
          "images": [
              {
                  "id": 51,
                  "project_id": 14,
                  "name": "2c44f849-03e1-443b-b122-ca9bd515c81f.png",
                  "old_name": "image1",
                  "type": "png",
                  "has_result": true,
                  "image_url": " http://127.0.0.1:8001/media/project_14/2c44f849-03e1-443b-b122-ca9bd515c81f.png",
                  "created_at": "2023-12-30T23:16:23.570664Z",
                  "updated_at": "2023-12-30T23:16:23.570712Z"
              },
              {
                  "id": 52,
                  "project_id": 14,
                  "name": "e8069482-fc9d-4e92-8574-7e7878218302.jpg",
                  "old_name": "image2",
                  "type": "jpg",
                  "has_result": true,
                  "image_url": " http://127.0.0.1:8001/media/project_14/e8069482-fc9d-4e92-8574-7e7878218302.jpg",
                  "created_at": "2023-12-30T23:16:23.603723Z",
                  "updated_at": "2023-12-30T23:16:23.603756Z"
              }
          ],
          "created_at": "2023-12-29T23:43:19.550344Z",
          "updated_at": "2023-12-31T10:33:07.718317Z"
      },
      {
          "id": 16,
          "name": "project4",
          "description": "this is project 4",
          "ai_model_id": 2,
          "customer_id": 6,
          "customer_username": "jier",
          "status": "COMPLETED",
          "images_nr": 0,
          "images": [],
          "created_at": "2023-12-31T08:37:27.969248Z",
          "updated_at": "2023-12-31T10:32:54.668839Z"
      },
  ]
  

  


### Retrieve A Single Project
- **Endpoint:** `/store/projects/<int:project_id>`
- **Method:** GET
- **Response Body (Example with project_id=14):**
  ```json
  {
      "id": 14,
      "name": "project3",
      "description": "this is a testing project3 hahaha",
      "ai_model_id": 2,
      "customer_id": 6,
      "customer_username": "jier",
      "status": "PENDING",
      "images_nr": 2,
      "images": [
          {
              "id": 51,
              "project_id": 14,
              "name": "2c44f849-03e1-443b-b122-ca9bd515c81f.png",
              "old_name": "image1",
              "type": "png",
              "has_result": false,
              "image_url": " http://127.0.0.1:8001/media/project_14/2c44f849-03e1-443b-b122-ca9bd515c81f.png",
              "created_at": "2023-12-30T23:16:23.570664Z",
              "updated_at": "2023-12-30T23:16:23.570712Z"
          },
          {
              "id": 52,
              "project_id": 14,
              "name": "e8069482-fc9d-4e92-8574-7e7878218302.jpg",
              "old_name": "image2",
              "type": "jpg",
              "has_result": false,
              "image_url": " http://127.0.0.1:8001/media/project_14/e8069482-fc9d-4e92-8574-7e7878218302.jpg",
              "created_at": "2023-12-30T23:16:23.603723Z",
              "updated_at": "2023-12-30T23:16:23.603756Z"
          }
      ],
      "created_at": "2023-12-29T23:43:19.550344Z",
      "updated_at": "2023-12-31T10:33:07.718317Z"
  }
  

### Create A Project
- **Endpoint:** `/store/projects/`
- **Method:** POST
- **Request Body (Example):**
  ```json
  {
    "name": "project3",
    "description": "this is a testing project3",
    "ai_model_id": 1
  }
- **Response Body (Example):**
  ```json
  {
      "id": 14,
      "name": "project3",
      "description": "this is a testing project3",
      "ai_model_id": 1,
      "customer_id": 6,
      "customer_username": "jier",
      "status": "PENDING",
      "images": [],
      "created_at": "2023-12-29T23:43:19.550344Z",
      "updated_at": "2023-12-29T23:43:19.550422Z"
  }
  
### Update A Project
- **Endpoint:** `/store/projects/<int:project_id>`
- **Method:** PATCH
- **Request Body (Example1):**
  ```json
  {
      "description": "p2222 tesing,  addition info"
  }
- **Request Body (Example2):**
  ```json
  {
    "ai_model_id": 2
  }

- **Response Body (Example):**
  ```json
  {
      "id": 11,
      "name": "p222",
      "description": "p2222 tesing,  addition info",
      "ai_model_id": 2,
      "customer_id": 6,
      "customer_username": "jier",
      "status": "PENDING",
      "images_nr": 0,
      "images": [],
      "created_at": "2023-12-29T23:31:04.922081Z",
      "updated_at": "2023-12-29T23:47:31.850663Z"
  }


### Delete A Single Project
- **Endpoint:** `/store/projects/<int:project_id>`
- **Method:** DELETE
- **Response HTTP status code:**
  ```text
  HTTP 204 No Content, A 204 status code indicates that the server has successfully processed the request, but there is no content to be returned to the client.




[//]: # (Images)
  

# API Design for Project Images
### Retrieve Image List of A Single Project
- **Endpoint:** `/store/projects/<int:project_id>/images/`
- **Method:** GET
- **Response Body (Example with project_id=1):**
  ```json
   [
      {
          "id": 23,
          "project_id": 1,
          "name": "p1_1",
          "old_name": "image1",
          "type": "png",
          "has_result": false,
          "image_url": " http://127.0.0.1:8001/media/project_1/p1_1.png",
          "created_at": "2023-12-22T10:11:41.657997Z",
          "updated_at": "2023-12-22T10:11:41.658044Z"
      },
      {
          "id": 24,
          "project_id": 1,
          "name": "p1_2",
          "old_name": "image2",
          "type": "jpg",
          "has_result": false,
          "image_url": " http://127.0.0.1:8001/media/project_1/p1_2.jpg",
          "created_at": "2023-12-22T10:11:41.680432Z",
          "updated_at": "2023-12-22T10:11:41.680485Z"
      }
  ]
  


### Retrieve A Single Image of A Single Project
- **Endpoint:** `/store/projects/<int:project_id>/images/<int:image_id>`
- **Method:** GET
- **Response Body (Example with project_id=1, image_id=23):**
  ```json
  {
    "id": 23,
    "project_id": 1,
    "name": "p1_1",
    "old_name": "image1",
    "type": "png",
    "has_result": false,
    "image_url": "http://127.0.0.1:8001/media/project_1/p1_1.png",
    "created_at": "2023-12-22T10:11:41.657997Z",
    "updated_at": "2023-12-22T10:11:41.658044Z"
  }


  

### Upload Images To A Single Project
- **Endpoint:** `/store/projects/<int:project_id>/images/`
- **Method:** POST
- **Request Body (Example):**
  ```text
  When uploading images for the frontend using an HTML form, make sure that the input element is set up. When using Postman, we need to create a POST request and include the image files in the request body, specifying "images" as the key for the file upload.
  ```
  ```json
  <input type="file" name="images" multiple>
  


- **Response Body (Example with project_id=9):**
  ```json
  {
      "data": [
          {
              "id": 98,
              "project_id": 9,
              "name": "51cf5020-d6da-4cd6-927c-eadd7f258879.png",
              "old_name": "image1",
              "type": "png",
              "image_url": "http://127.0.0.1:8001/media/project_9/51cf5020-d6da-4cd6-927c-eadd7f258879.png",
              "has_result": false,
              "created_at": "2024-01-21T00:18:45.621560+01:00",
              "updated_at": "2024-01-21T00:18:45.621613+01:00"
          },
          {
              "id": 99,
              "project_id": 9,
              "name": "cce0e206-965e-4059-879e-3be2e3b0dd41.jpg",
              "old_name": "image2",
              "type": "jpg",
              "image_url": "http://127.0.0.1:8001/media/project_9/cce0e206-965e-4059-879e-3be2e3b0dd41.jpg",
              "has_result": false,
              "created_at": "2024-01-21T00:18:45.663097+01:00",
              "updated_at": "2024-01-21T00:18:45.663132+01:00"
          }
      ],
      "error": false,
      "error_msg": "",
      "bad_images": []
  }
  

### Deleting An Image of A Single Project
- **Endpoint:** `/store/projects/<int:project_id>/images/<int:image_id>`
- **Method:** DELETE
- **Response Body(Example with project_id=9, image_id=98):**
  ```json
  HTTP 204 No Content
  {
      "message": "image with id 98 is deleted"
  }




[//]: # (Triggering)
  

# API Design for Image Processing
### Processing All Images of A Project
- **Introduction:**
  ```text
  After the endpoint is called, the frontend sends a request to the backend to trigger the processing of all images in the selected project using the chosen AI model. The backend will respond with a confirmation promptly.
  ```
- **Endpoint:** `/store/projects/<int:project_id>/start`
- **Method:** POST
- **Response Body (Example with project_id=7):**
  ```json
  {
    "message": "GOT IT, START PROCESSING"
  }



### Processing All Images of A Project
- **Introduction:**
  ```text
  When the endpoint is called, the frontend sends a request to the backend to process the remaining images in the selected project using the chosen AI model. The backend will promptly respond with a confirmation. This scenario assumes that a user may upload new images later, so there is no need to reprocess all images again.
  ```
- **Endpoint:** `/store/projects/<int:project_id>/start_rest`
- **Method:** POST
- **Response Body (Example with project_id=7):**
  ```json
  {
    "message": "GOT IT, START PROCESSING"
  }


[//]: # (Result Set)
  

# API Design for ResultSet
### Retrieve Result Sets List of A Project
- **Endpoint:** `/store/projects/<int:project_id>/results/`
- **Method:** GET
- **Response Body (Example with project_id=19):**
[Link](./steps_example_project_19/step4_get_result_set/project_19_resultset.json)
  


### Retrieve Result Set of An Image of A Project
- **Endpoint:** `/store/projects/<int:project_id>/results/<int:image_id>`
- **Method:** GET
- **Response Body (Example with project_id=19, image_id=55):**
[Link](./steps_example_project_19/step4_get_result_set/project_19_image_55.json)
  

  


















