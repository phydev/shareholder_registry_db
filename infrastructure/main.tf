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

resource "docker_image" "minio_image" {
  name         = "quay.io/minio/aistor/minio:RELEASE.2026-08-07T18-34-35Z"
  keep_locally = true
}

resource "docker_image" "unitycatalog_image" {
  name         = "unitycatalog/unitycatalog"
  keep_locally = true
}

resource "null_resource" "build_ui_with_volume" {
  provisioner "local-exec" {
    command = <<EOT
      mkdir -p ${var.home_dir}/.podman-build-cache

      podman build \
        -v  ${var.home_dir}/.podman-build-cache:/var/lib/containers/storage/overlay-layers/tmp:O \
        -t localhost/unitycatalog-ui:latest \
        ${var.unitycatalog_ui_path}
    EOT
  }
}