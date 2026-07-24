terraform {
  backend "s3" {
    bucket = "terraform-state-observability"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"
  }
}