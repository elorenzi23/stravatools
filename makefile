# Define the name of the virtual environment
VENV_NAME = venv

# Define the name of the Docker image
DOCKER_IMAGE = myproject_image

# Create and activate virtual environment, and install requirements
.PHONY: venv
venv:
	# Create virtual environment if it doesn't exist
	python3 -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements-dev.txt

# Build Docker image
.PHONY: build-docker
build-docker:
	# Build the Docker image using the Dockerfile
	docker build -t $(DOCKER_IMAGE) .

# Install requirements inside the virtual environment
.PHONY: install
install:
	# Install dependencies inside the virtual environment
	$(VENV_NAME)/bin/pip install -r requirements-dev.txt

# Run application with Docker
.PHONY: run-docker
run-docker:
	# Run the Docker container with the specified image
	docker run -p 8000:8000 $(DOCKER_IMAGE)

# Clean up: remove virtual environment
.PHONY: clean-venv
clean-venv:
	# Remove virtual environment folder
	rm -rf $(VENV_NAME)

# Clean up: remove Docker image
.PHONY: clean-docker
clean-docker:
	# Remove Docker image
	docker rmi $(DOCKER_IMAGE)

# Install the requirements and then build the Docker image
.PHONY: install-and-build
install-and-build: venv install build-docker

test:
	pytest --cov=app tests/

lint:
	black .
	ruff check . --fix
	flake8 . --exclude=venv
	isort .

#keeping mypy checks separate for now
typecheck:
	mypy .


