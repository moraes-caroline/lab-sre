resource "aws_instance" "this" {

  ami                    = var.ami_id
  instance_type          = var.instance_type
  vpc_security_group_ids = [var.security_group_id]

  iam_instance_profile   = var.instance_profile_name

  user_data = var.user_data

  tags = {
    Name = var.instance_name
  }
}