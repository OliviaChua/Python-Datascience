PROJECT = python_datascience
IMAGE ?= jupyter/datascience-notebook

PYTHON ?= python3
.PHONY: all build run
HOST_DIR = $(shell pwd)/workspace

MOUNT_HOST_DIR = -v $(HOST_DIR):/home/jovyan/work

all: run

# Run the container and expose the container port 7000 and bind to client's port 7070
run:
	docker run -it --rm --name $(PROJECT) $(MOUNT_HOST_DIR) -p 8888:8888 $(IMAGE)

