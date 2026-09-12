resource "aws_db_instance" "customers" {
  identifier        = "customers"
  engine            = "postgres"
  storage_encrypted = false
  publicly_accessible = false
}
