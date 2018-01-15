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
While not strictly required to develop, it's probably a Good Idea. In the root directory
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

Like any django app, the server can be run with
```sh
python manage.py runserver
```
and a shell can be started to mess around with via
```sh
python manage.py shell
```
See the django docs for all the available options.