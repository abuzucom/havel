resource "aws_s3_bucket" "user_uploads" {
  bucket = "acme-user-uploads"
}

resource "aws_dynamodb_table" "sessions" {
  name         = "sessions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "session_id"
}
