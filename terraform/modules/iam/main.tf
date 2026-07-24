resource "aws_iam_role" "ec2_role" {

  name = "observability-role"

  assume_role_policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {

        Action = "sts:AssumeRole"

        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

      }

    ]

  })

}

resource "aws_iam_role_policy_attachment" "cloudwatch" {

  role = aws_iam_role.ec2_role.name

  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"

}

resource "aws_iam_instance_profile" "profile" {

  name = "observability-profile"

  role = aws_iam_role.ec2_role.name

}