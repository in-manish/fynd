Technology Stack
---

    Python 3.8
    Django 3.2.7
    Postgresql 13.3
    djangorestframework 3.12.4

Running Project
----

Create a virtualenv

```shell
$virtualenv venv
```

Activate the environment

```shell
$source venv/bin/activate
```

Install dependencies

```shell
$pip install -r requirements.txt
```

Go to project directory

* create log directory and file

```shell
  $ mkdir logs
  $ cd logs
  $ touch debug.log
```

* migrate database

```
python manage.py migrate
 ```

Run local server

```shell
python manage.py runserver
```

Created superuser

```shell
python manage.py createsuper
```

<hr>

### [APIs Docs](http://13.232.245.139/redoc/)
