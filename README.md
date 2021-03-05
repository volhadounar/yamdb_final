https://github.com/volhadounar/yamdb_final/workflows/main/badge.svg

Service Yamdb
=================================

In a team with my colleagues we have written service – databases of reviewing films, books, music and
REST API for it. My role included registration and authentication system, access rights, work with a token, e-mail confirmation system.

The project is deployed at a remote server, see documentation on  http://84.201.177.212/redoc/ or http://ilza-yamdb.tk/redoc/, or http://www.ilza-yamdb.tk/redoc/. Follow admin site http://ilza-yamdb.tk/admin/ using credentials: email:admin@live.com, password:admin.

Tech stack: Python3, Django Rest Framework, HTTP, HTTPS, PostgreSQL, Gunicorn, Nginx, Linux, Docker, Postman, Visual Studio Code, Yandex Cloud, GitHubActions.

Getting Started
===============

1. You can build it in steps:
    1. ``cd ...wherever...``
    2. ``git clone https://github.com/volhadounar/yamdb_final.git``
    3. ``cd yamdb_final``
    4. ``docker-compose up``
    5. Open another command window.
    6. ``docker-compose run web python manage.py migrate`` -- Reads all the migrations folders in the application folders and creates / evolves the tables in the database
    7. ``docker-compose exec web python manage.py createsuperuser``
    8. ``docker-compose exec web python manage.py loaddata fixtures.json`` -- Uploads fixtures file with web-service' data
2. The usage in Postman:
    1. http://localhost/redoc/ -- Read documentation in browser
    2. E-mail confirmation:
        - In Postman make put request with body {"email":"some_email"} using:
        http://localhost/api/v1/auth/email/
        - Find confirmation code in the folder 'sent_emails'. Use it in the next step.
        - Make put request with body {"email":"some_mail", "confirmation_code": "some_confcode_from_email"}:
        http://localhost/api/v1/auth/token/
        - Input token in the request headers: `Authorization: Bearer <token>`
        - http://localhost/api/v1/users/me/ -- Fetch your current profile data




