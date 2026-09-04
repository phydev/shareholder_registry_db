
resource "docker_container" "storage_layer" {
  image = docker_image.minio_image.image_id
  name  = "storage_layer"
  networks_advanced {
    name = docker_network.network_layer.name
  }
  ports {
    internal = 9000
    external = 9000
  }
  ports {
    internal = 9001
    external = 9001
  }
  volumes {
    host_path      = "${var.home_dir}/minio/data"
    container_path = "/mnt/data"
  }
  volumes {
    host_path      = "${var.home_dir}/minio/minio.license"
    container_path = "/minio.license"
  }
  volumes {
    host_path      = "${var.home_dir}/minio/certs"
    container_path = "/etc/minio/certs"
  }

  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]

  # Run arguments passed to the container entrypoint
  command = [
    "server",
    "/mnt/data",
    "--license",
    "/minio.license"
  ]

}
