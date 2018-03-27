# apollo-core

[![Build Status](https://travis-ci.com/phansen01/apollo-core.svg?token=NMf6bwTExjejsyWqoTBy&branch=master)](https://travis-ci.com/phansen01/apollo-core)

The backend of our shared space reservation platform.

## Setup

### `pip`
First, [install pip](https://pip.pypa.io/en/stable/installing/). 
I don't think it matters whether pip2 or pip3 since we just need it to pull
down `virtualenv`, then all other dependencies will live inside that virtual environment.

### `virtualenv`
Install with
```sh
pip install virtualenv
```
I'm currently using `virtualenv` to make development consistent and manage dependencies.
While not strictly required to develop, it's probably a Good Idea. 

First, you'll need a python3 installation. On macOS this can be done via
```sh
brew install python3
```
(or various other ways).
Next, in the root directory
of the git repo, do
```sh
virtualenv --python=python3 env
```
to get an environment set up. Whenver you want to use the virtual environment (to develop),
just do
```sh
source env/bin/activate
```

### Installing and Managing Dependencies
Inside the virtual environment, just run
```sh
pip install -r requirements.txt
```

If a new dependency is needed, it can be installed with pip and then `pip freeze` will update
the dependencies (`requirements.txt`).

## Running
Before starting a local instance, environment variables must be set, and the SQL proxy must be started. (See Deployment section for additional details.)

```sh
source env_vars.sh
./start_sql_proxy
```

Like any django app, the server can be run with
```sh
python manage.py runserver
```
and a shell can be started to mess around with via
```sh
python manage.py shell
```
See the django docs for all the available options.

## Deployment

Production deployment of this application is configured for use with Google Cloud Platform.
The Apollo Application is served by a [App Engine Python 3 Flexible Runtime](https://cloud.google.com/appengine/docs/flexible/python/), static content is served from [Cloud Storage](https://cloud.google.com/storage/docs/), and structured data is managed by a PostgresSQL database on [Cloud SQL](https://cloud.google.com/sql/docs/postgres/).

For latency optimization for a Expo Demo in Chicago, the application is hosted in the [us-central1 region](https://cloud.google.com/about/locations/), which is one state West in Iowa.

### Google Cloud Platform Dependencies
Working with GCP services requires the installation of the namesake SDK, and a proxy script for
connecting to a hosted database.

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
- [Cloud SQL Proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy)

### Integration with Frontend Component.
Django is also used to serve frontend content found in the apollo-ui project via the [django-webpack-loader](https://github.com/ezhome/django-webpack-loader) module.
Build the frontend via webpack, put the webpack-stats.json in the project root directory, and the bundles in /assets/bundles. If this is unclear, look at .gitignore for details.

### Deploying to Production
Before deploying a new version of the application, static assets must be collected and uploaded.
As with other django management commands, this will fail if environment variables have not been set.
```sh
python manage.py collectstatic
./sync_static.sh
```
Once static files are uploaded, the app itself can be deployed.
```sh
gcloud app deploy
```