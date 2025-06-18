Project Name: Python Machine Test

This is a Django-based Project Management System that allows users to manage projects, clients, and team members.
The system has been developed using Django Rest Framework and connects to a MySQL database.

Steps to Set Up and Run the Project

1. Set Up a Virtual Environment- (Optional)
It is recommended to use a virtual environment to manage dependencies. If you don't have virtualenv installed, install it using the following:
"pip install virtualenv"
Create and activate a virtual environment:
"virtualenv venv
.\venv\Scripts\activate"

2. Install Required Dependencies
Once the virtual environment is activated, install the required dependencies using the requirements.txt file:
"pip install -r requirements.txt"

3. Create a Django project:
"django-admin startproject client_project"
"cd client_project"

4. Create an application:
"python manage.py startapp api"

5. Add the app to INSTALLED_APPS in settings.py:
Example:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # rest framework
    'api',  # Your new app
]

6. Set Up the Database
Make sure you have a MySQL server running. Create a database for the project, and update the database settings in settings.py:
Open project_name/settings.py (where project_name is the name of your Django project).
Update the DATABASES section with your database credentials.
Example:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

7.  Define Models - In api/models.py

8. Run migrations:
"python manage.py makemigrations"
"python manage.py migrate"

9. Create Serializers - In api/serializers.py

10. Create Views - In api/views.py

11. Define URLs - In api/urls.py

12. Define the api urls in client_project/urls.py

13. Create a Superuser (Admin) - "python manage.py createsuperuser"

14. Run the APIs -
Run the server:"python manage.py runserver"

15. Access the Django Admin Panel
To manage projects, clients, and users, you can log into the Django admin panel:

URL: http://127.0.0.1:8000/admin/
Username and Password: The superuser credentials you created.

Database Design

Project Table
id: Primary key
project_name: Name of the project
client: Foreign key to the Client table
created_at: Date and time the project was created
created_by: User who created the project
updated_at: Date and time the project was last updated

Client Table
id: Primary key
client_name: Name of the client
created_at: Date and time the client was created
created_by: User who created the client
updated_at: Date and time the client was last updated
User Table (Assuming you use Django's built-in User model)

id: Primary key
username: Username of the user
password: Password of the user
email: Email address of the user

