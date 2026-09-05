variable "db_postgres" {
  type = string
  sensitive = false
}

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

variable "db_port" {
  type      = string
  sensitive = false
}

