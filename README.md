# geoshop2

## Requirements

* PostgreSQL > 10 + PostGIS
* Python 3.6 / 3.7
* pipenv (pip install pipenv)
* GDAL 2.4 (see instructions below to install it in your venv)

## Getting started


Fork and clone this repository. Make a copy of the `.env` file and adapt it to your environment settings:

```powershell
cd back
cp .env.sample .env
cd..
```

### Database

User geoshop is assumed to be already created. Set up a database manually or with the provided script in `scripts/create_db.ps1` (psql binary must be on PATH) :

```sql
CREATE DATABASE geoshop;
CREATE EXTENSION postgis;
CREATE SCHEMA geoshop AUTHORIZATION geoshop;
```

### Backend

Install the app. If you want your `venv` to be inside your project directory, you need to set `PIPENV_VENV_IN_PROJECT` environment variable, otherwise it'll go to your profile:

```powershell
cd back
$env:PIPENV_VENV_IN_PROJECT="True"
pipenv install --dev           # installs everything needed
pipenv shell                   # activates venv and reads .env file
```

#### Installing GDAL on Windows
Download the GDAL 2.4 wheel (3.X isn't supported yet by Django) on this page: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal. For example, if you have Python 3.6 64bit, choose `GDAL‑2.4.1‑cp36‑cp36m‑win_amd64.whl`.
Then install it weather system wide or in your venv (the example below will show the venv variant and expects you have your venv activated):

```powershell
pip install path\to\your\GDAL-2.4XXXX.whl
```

You'll then need to add GDAL dll to your PATH if you installed it system wide. You can get the dll path with:

```python
python

from pathlib import Path, PureWindowsPath
from osgeo import gdal

print(PureWindowsPath(gdal.__file__).parent)
```

Otherwise, if you installed it in your venv, configure `.env` properly.

### Migrate and run

You should now be able to run migrations:

```powershell
python manage.py migrate
```

If you're starting with a fresh new database you'll need to create an user or restore a dump:

```powershell
python manage.py createsuperuser --email admin@example.com --username admin
```

Your database should be ready, now you can run the backend:

```powershell
python manage.py runserver
```

Translations can be generated with:

```powershell
python manage.py compilemessages
```

### Frontend

Install the current LTS version of [Nodejs](https://nodejs.org/en/).

Install @angular/cli and typescript globally

```powershell
npm install -g @angular/cli typescript
```

Install the dependances of the frontend

```powershell
cd front
npm install
```

To start the debug of the frontend

```powershell
npm start
```

Then open a browser and go to [Geoshop2](http://localhost:4200)


## Deploy

collect static files:

```powershell
python .\manage.py collectstatic
```

configure apache

```apache
Alias /back_enpoint/static "/path/to/folder/back/static/"
<Directory "/path/to/folder/back/static/">
    Require all granted
</Directory>

WSGIScriptAlias /back_enpoint /path/to/file/back/apache/app.wsgi

<Directory /path/to/file/back/apache>
    <Files app.wsgi>
		    Require all granted
	  </Files>
</Directory>
```
