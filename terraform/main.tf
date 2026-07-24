module "iam" {

  source = "./modules/iam"

}

module "security_group" {

  source = "./modules/security-group"

  instance_name = var.instance_name
  allowed_ip    = var.allowed_ip
  environment   = var.environment

}

module "ec2" {

  source = "./modules/ec2"

  ami_id        = var.ami_id
  instance_type = var.instance_type
  instance_name = var.instance_name
  environment   = var.environment

  security_group_id = module.security_group.security_group_id

  instance_profile_name = module.iam.instance_profile_name

  user_data = file("${path.root}/userdata.sh")

}