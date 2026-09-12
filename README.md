# Shareholder Registry Database
Longitudinal database for Aksjonærregisteret: https://www.skatteetaten.no/deling/aksjonarregisteret/

This repository contains the data model for registry, an ingestion pipeline, and the infrastructure as code. The next 
steps in the project are developing the API and the frontend application for lookup.

# Table of contents
- [Requirements](#requirements)
- [Get started](#get-started)

# Requirements
- python: 3.13
- dependency manager: uv
- database: postgres
- engine: SQLModel
- infra: terraform + podman


# Get started

## Dependency manager
We use [uv](https://docs.astral.sh/uv/) as dependency manager. 
It works in a similar way as poetry, but it is faster and solves dependencies efficiently. 
Read the installation guide [here](https://docs.astral.sh/uv/#installation).

After the installation, run the following command from the project folder:
```bash
uv sync
```

Then start the API:
```bash
uv run python -m src.api.main;
```
The documentation should be available at http://0.0.0.0:8080/docs. 

## Infrastructure-as-Code 
The infrastructure is defined with terraform under the folder `/infrastructure`. 

## Building & Deploying the application 
You can build the application and the deploy to podman with two commands:
```bash
make deploy # build the image and register to podman
make tf-deploy # deploy the application container and the postgresdb
```
Check the [Makefile](Makefile) if you want to look into the details.
