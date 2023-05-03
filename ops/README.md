# Docker configurations

## Preamble: logins

### Buildwise's GitHub Container Registry

In order to **push** and **pull** images to and from [Buildwise's GitHub Container Registry](https://github.com/orgs/CSTC-WTCB-BBRI/packages), you need to be logged in:

* In your GitHub settings go to "Developer settings > Personal access tokens > Tokens (classic)", and click on "Generate new token > Generate new token (classic)";
* Give it whatever name and expiration you wish;
* Select the "write:packages" scope;
* The "read:packages" and "repo" scopes should automatically have been selected;
* Click "Generate token";
* Before leaving the page, save your newly generated token somewhere! You won't ever be able to consult it again otherwise, therefore you would need to generate a new one...
* In your console, run `docker login ghcr.io` and log in using your GitHub username and the previously generated token as password;

## Base image ([/ops/base](./base))

The purpose of the base image is mostly to speed up the building of the working images.

It contains dependencies (binaries, gems, etc.) common to the various environments (local development/test, feature, staging, production, etc.).

It must be rebuilt and pushed to the Docker registry whenever the base Dockerfile is modified (e.g. when the Python version is updated, when binaries are added, etc.). It is also a good idea to rebuild and push a new version from time to time in order to install new or updated python packages in the base image (this is not mandatory, but as explained above it will speed up the building of the working images).

The base image can be built and pushed using the following command:

```bash
# from the project's root directory:
TAG=NEW_TAG ./ops/base/build
```

**NOTE**: Running the `build` script without a new tag will use the *latest* tag.

**NOTE**: When pushing a new image tag, the Dockerfiles you want to use the new image tag have to be updated accordingly. After having completed the previous example command, the [dev Dockerfile](./dev/Dockerfile) should be edited with the new tag:

```docker
FROM ghcr.io/cstc-wtcb-bbri/spotutils.base:NEW_TAG

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
```

Most of the time, developers should not worry about the base image, as an up-to-date version should be available on GitHub and will be pulled automatically when building the dev and test images.

## Development ([/ops/dev](./dev))

This directory contains all that should be needed to run the application stack locally with Docker.

### Setup

Create a `app_env.secrets` file in the `/ops/dev` directory. This files is ignored by Git and will allow you to override
the environment variables defined by default in `app_env` if needed.

All values left blank in the `app_env` file *must* be set in this new file.

**NOTE**: Running the `dev` script creates an **empty** `app_env.secrets` file, if it does not already exist.

**NOTE**: Refer to this project's [main README document](../README.md), specifically the [Environment Variables](../README.md#environment-variables) and [Development Payload](../README.md#development-payload) sections for information about the `SELF_IP`, `GUID` and `SECRET` variables.

#### Setup Database And Django Superuser

Before anything else below, run the following two commands:
```bash
./dev run --rm app python manage.py migrate
./dev run --rm app python manage.py createsuperuser
```

The second command will prompt you to enter credentials for the superuser. There are no *right* or *wrong* answer and this will not impact the application functionalities. **Remember them though!**

**NOTE**: You will need to run that again if you wipe out the *kvstore_data* volume.

### Running the application

Running the following from the project root directory will start all the Django service.

```bash
# run docker compose attached to the foreground:
./dev up
# run docker compose in detached mode:
./dev up -d
# run docker compose while forcing a rebuild of the images
./dev up --build
```

**NOTE**: The above arguments can be combined. For example: `./dev up -d --build`.

The `dev` script simply allows you to run Docker Compose commands from the project's root directory, even though the Docker and Docker Compose files are located elsewhere. 

Refer to the official [Overview of docker compose CLI](https://docs.docker.com/compose/reference/) for more detailed instructions.

**NOTE**: The very first time you run the `dev` script, an empty file named `app_env.secrets` will be created in
the `ops/dev` directory, provided you did not already went over the [Setup](#setup) section above.

To access the *development web application*, follow [this](http://127.0.0.1:8000) link.

To access the **API endpoints**, follow [this](http://127.0.0.1:8000/api/) link.

**NOTE**: The provided links only works if you **did not change the ports** in the `docker-compose.yml` file.

### Override configuration

If for some reason you want to tweak the provided Docker Compose configuration in order to better suit your local setup, the recommended way is to create, in the same directory, a `docker-compose.override.yml` file in which you can specify your own configuration. This file is ignored by Git and is automatically taken into account by Docker Compose. 

For example:

```docker
services:
  app:
    volumes:
      - test_volume:/app/test_volume

volumes:
  test_volume:
```

**NOTE**: You do not need to rewrite everything, only the things that change (refer to the [official Docker documentation](https://docs.docker.com/compose/extends/#understanding-multiple-compose-files)).
