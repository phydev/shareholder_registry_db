
resource "docker_container" "postgresdb" {
  image = docker_image.postgres_image.image_id
  name  = "datawarehouse"
  networks_advanced {
    name = docker_network.network_layer.name
  }

  ports {
    internal = 5432
    external = 5432
  }
  env = [
    "POSTGRES_DB=metadata_db",
    "POSTGRES_USER=${var.db_admin_user}",
    "POSTGRES_PASSWORD=${var.db_admin_password}",
    "POSTGRES_HOST=${var.db_host}"
  ]
}