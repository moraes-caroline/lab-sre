resource "aws_security_group" "this" {

  name = "${var.instance_name}-sg"

  ingress {

    from_port = 80
    to_port = 80
    protocol = "tcp"

    # Restrict HTTP access to the allowed IP range provided via variable
    cidr_blocks = [var.allowed_ip]

  }

  ingress {

    from_port = 22
    to_port = 22
    protocol = "tcp"

    cidr_blocks = [var.allowed_ip]

  }

  egress {

    from_port = 0
    to_port = 0
    protocol = "-1"

    cidr_blocks = ["0.0.0.0/0"]

  }

}