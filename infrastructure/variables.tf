variable "db_admin_user" {
  type      = string
  sensitive = true
}

variable "db_admin_password" {
  type      = string
  sensitive = true
}

variable "db_host" {
  type      = string
  sensitive = false
}

variable "home_dir" {
  type      = string
  sensitive = false
}

variable "minio_root_user" {
  type      = string
  sensitive = true
}

variable "minio_root_password" {
  type      = string
  sensitive = true
}

variable "unitycatalog_ui_path" {
  type      = string
  sensitive = false
}