resource "aws_security_group" "metabase-acess" {

    ingress {

        from_port = 3000
        to_port = 3000
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]

    }

    ingress {

        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]

    }

    egress {

        from_port = 0
        to_port = 0
        protocol = "-1"
        self = true

    }

    ingress {

        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]

    }


}

resource "aws_instance" "metabase-app" {

    ami = "ami-01e5ff16fd6e8c542"
    instance_type = "t3.medium"
    user_data = "${file("setup.sh")}"
    key_name = "general-usage-key"
    vpc_security_group_ids = [aws_security_group.metabase-acess.id]
    associate_public_ip_address = true

    tags = {

        Name = "metabase - Debian"
        Env = "Dev"

    }

}

output "ec2-instance-adress" {

    value = aws_instance.metabase-app.public_ip
  
}