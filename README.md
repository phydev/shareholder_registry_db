# shareholder_registry_db
Longitudinal database for Aksjonærregisteret: https://www.skatteetaten.no/deling/aksjonarregisteret/


## Setup
### DuckDB
Visit [duckdb](https://duckdb.org/install/?platform=macos&environment=cli) and follow the instructions for your operative system.


## Infrastructure-as-Code
The infrastructure is defined with terraform under the folder `/infrastructure`. 

### Deploying application image to podman
Run `make build` to build the image and `make deploy` deploy to podman registry:
```bash
podman build -t backend-registry .
```

### Deploy containers
Run `terraform apply` to update the container with the new image. Or deploy only backend and database:
```bash
terraform apply -target=docker_container.backend -target=docker_container.postgresdb
```

## Accessing the API
The application is deployed on https://localhost:8080