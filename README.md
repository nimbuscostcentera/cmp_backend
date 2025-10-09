# Django Project

This is a Django backend project with multiple apps (`masters`, `myauth`, `cmp`).  
It includes REST API functionality, JWT authentication, and media file handling.

---

## Project Structure

project_root/
│
├── masters/ # Django app
├── myauth/ # Django app
├── cmp/ # Django app
├── project_name/ # Django project settings, urls, wsgi
├── media/ # Uploaded media files (ignored in Git)
├── manage.py
├── requirements.txt
└── .gitignore

yaml
Copy code

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your_repo_url>
cd <project_root>
2. Create a virtual environment
bash
Copy code
# Linux / Mac
python -m venv env
source env/bin/activate

# Windows
python -m venv env
env\Scripts\activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure environment variables
Create a .env file in the project root (not included in Git) and add:

ini
Copy code
SECRET_KEY=<your_django_secret_key>
DEBUG=True
DATABASE_NAME=<your_db_name>
DATABASE_USER=<your_db_user>
DATABASE_PASSWORD=<your_db_password>
DATABASE_HOST=localhost
DATABASE_PORT=5432
You can use python-decouple or django-environ to load .env variables.

5. Run migrations
bash
Copy code
python manage.py migrate
6. Create a superuser (optional)
bash
Copy code
python manage.py createsuperuser
7. Run the server
bash
Copy code
python manage.py runserver
The backend will be available at http://127.0.0.1:8000/.