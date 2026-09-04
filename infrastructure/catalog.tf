resource "docker_container" "unity_catalog" {
  image = docker_image.unitycatalog_image.image_id
  name  = "unity_catalog"
  networks_advanced {
    name = docker_network.network_layer.name
  }

  ports {
    internal = 8080
    external = 8888
  }
}