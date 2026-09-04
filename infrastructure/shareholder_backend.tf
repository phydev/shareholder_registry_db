resource "docker_container" "ar_backend" {
  image = docker_image.registry_image.image_id
  name  = "ar-backend"
  networks_advanced {
    name = docker_network.network_layer.name
  }
  env = [
    "POSTGRES_DB=metadata_db",
    "POSTGRES_USER=${var.db_admin_user}",
    "POSTGRES_PASSWORD=${var.db_admin_password}",
    "POSTGRES_HOST=${var.db_host}"
  ]

  ports {
    internal = 8080
    external = 8080
  }

  depends_on = [
    docker_container.postgresdb
  ]
}


