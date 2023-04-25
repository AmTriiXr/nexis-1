# Nexis

Nexis is a web application built to provide users with a platform to search for news articles, read them, and save them for future reference.

## Preview

To see the application in action, you can visit [nexis.herokuapp.com](https://nexis.herokuapp.com).

## How to Start the Project

To get started with the project, follow these steps:

- Create a virtual environment by running `python -m venv <name_env>`. If your operating system is Linux or MacOS, you can activate the virtual environment by running `source <name_env>/bin/activate`.
- Install the dependencies listed in `requirements.txt` by running `pip install -r requirements.txt`.
- After installing the dependencies, run the migrations by executing `python manage.py migrate` in the terminal.
- Finally, run `python manage.py collectstatic --noinput` to collect all static files, and start the server by running python manage.py runserver.

## How to Sertup Database?

Once you have installed PostgreSQL, you can proceed with the following steps to set up the database for Nexis:

- Create a new PostgreSQL database for the project.
- In the project directory, open the settings.py file and locate the DATABASES configuration. Replace the existing database configuration with the following:

```python
DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': '<your_database_name>',
          'USER': '<your_database_username>',
          'PASSWORD': '<your_database_password>',
          'HOST': 'localhost',
          'PORT': '',
      }
  }
```

- Replace `<your_database_name>`, `<your_database_username>`, and `<your_database_password>` with your own credentials.

- Run the following command to apply the database changes: `python manage.py migrate`.

That's it! Your database is now set up and ready to use with Nexis. If you encounter any issues during this process, please refer to the Django documentation or seek help from the Django community.

Thank you for using Nexis!
