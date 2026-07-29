terraform {
  backend "s3" {
    bucket = "terraform-state-observability-035885606922"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"
  }
}
