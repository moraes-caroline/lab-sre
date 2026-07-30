variable "aws_region" {
  type = string
}

variable "environment" {
  type = string
}

variable "instance_name" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "instance_profile_name" {
  type = string
}

variable "ami_id" {
  type = string
}

variable "allowed_ip" {
  type    = string
  default = "0.0.0.0/0"
}

