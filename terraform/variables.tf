variable "aws_region" {
  type = string
  default = "us-east-1"
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
  default = "ami-02b64aa047cb5edf5"
}

variable "allowed_ip" {
  type    = string
  default = "0.0.0.0/0"
}

