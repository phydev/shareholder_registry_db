terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
}

# Create a shared network
resource "docker_network" "network_layer" {
  name = "network_layer"
}

resource "docker_image" "postgres_image" {
  name         = "postgres:trixie"
  keep_locally = true
}

resource "docker_image" "registry_image" {
  name         = "localhost/backend-registry:latest"
  keep_locally = false
}

