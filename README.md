# Tubble Digital Bucket List Application

Tubble is a travel bucket list app that enables users to create, save, and track destinations. It offers features such as creating user accounts, the ability to save blog posts to favorites, write blog comments, a REST API, profile management, viewing other users' profiles, and destination filtering capabilities.

Built with: 
* Python
* Django
* Bootstrap
* PostgresSQL
* PythonAnywhere

## 🎥 Video Preview

https://user-images.githubusercontent.com/101557392/214550076-eba8123e-0365-44fd-b7dc-067ae56321f9.mp4

## 👩‍🔧 Getting Started 

These instructions will provide you a copy of the project that you can run locally. Visit [PythonAnywhere](https://pythonanywhere.com/ "PythonAnywhere") to set up a free account if you would like to host.

## 🛠️ Install

**Step 1:** Open Git Bash and change the current working directory to the location where you want the cloned directory. 
```python
git clone git@github.com:vwingardh/tubble.git
```

**Step 2:** Create a virual environment for web app.
```python
python -m venv venv
```

**Step 3:** Activate virtual environment with following command.
```
venv\Scripts\activate
```

**Step 4:** Install all packages in requirements.txt file in project directory.
```python
pip install -r requirements.txt
```

**Step 5:** By default Django uses SQLite, this app uses PostgreSQL. To use SQLite, change the database code in settings.py to: 
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Otherwise, create a PostgreSQL database using pgAdmin and configure NAME and PASSWORD to that of your newly created PostgreSQL database.

**Step 6:** Generate a new secret key and add to SECRET_KEY in settings.py. Run key_generator.py to generate a new key or use [Djecrety](https://djecrety.ir/ "Djecrety") to generate a secret key.

**Step 7:** Create a .env file in the root directory (where manage.py is) to secure secret key and database credentials.

**Step 8:** Delete existing migrations and migrate to new database.
```python
python manage.py makemigrations

python manage.py migrate
```

**Step 9:** Create a superuser for access to the admin panel.
```python
python manage.py createsuperuser
```

**Step 10:** Start the development server and ensure there are no errors.
```python
python manage.py runserver
```

That's it, you're all set!
