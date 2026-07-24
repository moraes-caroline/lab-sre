variable "role_name" {
  description = "Nome da IAM Role"
  type        = string

  default = "observability-role"
}

variable "instance_profile_name" {
  description = "Nome do Instance Profile"
  type        = string

  default = "observability-profile"
}