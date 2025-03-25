# Template Python Webapp Repo

This repository is meant to be a jumping off point for python projects that use the fastAPI library for easy API definition, SQLAlchemy for object relational mapping, and Streamlit for data visualization. Please feel free to use it for your own projects if it suits your needs. 
## Features
[**fastApi:**](https://fastapi.tiangolo.com/) This python library allows for the simple definition of api endpoints for your webapp.
 
[**SQLAlchemy:**](https://www.sqlalchemy.org/) Provides Object Relational Rapping for easier interaction with the database from within your Python application.

[**Streamlit:**](https://streamlit.io/) Allows developers to create web apps using only Python, without requiring HTML, CSS, or JavaScript 

[**Alembic:**](https://alembic.sqlalchemy.org/en/latest/) Database migration tool for use with SQLAlchemy. 

[**Docker:**](https://www.docker.com/) Dockerfile builds a simple docker image of the webapp.

[**make:**](https://man7.org/linux/man-pages/man1/make.1.html) Makefile includes commands to activate the virtual environment, install dependencies, build the docker image, and run linting. 

**linting:** Uses [black](https://github.com/psf/black) and [ruff](https://github.com/astral-sh/ruff) to format code, and [mypy](https://mypy-lang.org/) to ensure typechecking. 

[**Github Actions:**](https://github.com/features/actions) Ensures that pushed code passes unit tests and linting, and that Docker image builds. 

[**Pytest:**](https://docs.pytest.org/en/stable/) Used to manage unit testing. 

##  Instructions
Once you clone this repo, you will need to update your secrets on Github to include your Docker username and password. If you don't wish to have Github actions push your image to Docker Hub, you can edit the "docker" task in /github/workflows/python-tests.yaml.

## Notes and Todos
Currently, I am using the dotenv library to allow for easy configuration of separate databases. However, in the test and github actions code, the database is hardcoded to the test.db file used by sqllite. I am working on determining the best path forward for this. 

