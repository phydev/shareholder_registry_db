resource "docker_container" "ar_backend" {
  image = docker_image.registry_image.image_id
  name  = "ar-backend"
  networks_advanced {
    name = docker_network.shared_network.name
  }
  env = [
    "POSTGRES_DB=${var.db_postgres}",
    "POSTGRES_USER=${var.db_admin_user}",
    "POSTGRES_PASSWORD=${var.db_admin_password}",
    "POSTGRES_HOST=${var.db_host}",
    "POSTGRES_PORT=${var.db_port}"
  ]

  ports {
    internal = 8080
    external = 8080
  }

  depends_on = [
    docker_container.postgresdb
  ]
}


