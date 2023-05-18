resource "aws_security_group" "rds-acess" {

    ingress {

        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

}

resource "aws_db_instance" "rds-postgres-instance" {
  
    db_name = "server01"
    engine = "postgres"
    engine_version = "14.3"
    instance_class = "db.t3.micro"
    username = var.username
    password = var.password
    skip_final_snapshot = true
    identifier = "${var.proj-name}-postgres"
    allocated_storage = 20
    max_allocated_storage = 50
    vpc_security_group_ids = [aws_security_group.rds-acess.id]
    publicly_accessible = true

}

output "database-host" {
  
    value = aws_db_instance.rds-postgres-instance.address

}

output "username" {

    value = aws_db_instance.rds-postgres-instance.username
  
}

output "password" {

    value = aws_db_instance.rds-postgres-instance.password
    sensitive = true
  
}