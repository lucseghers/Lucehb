provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "existing_bucket" {
  bucket = "lucseghers03"
  acl    = "private"

  tags = {
    Name        = "lucseghers03"
    Environment = "Dev"
  }
}

# Optionally define a bucket policy
resource "aws_s3_bucket_policy" "existing_bucket_policy" {
  bucket = aws_s3_bucket.existing_bucket.bucket

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:GetObject"]
        Effect = "Allow"
        Resource = ["${aws_s3_bucket.existing_bucket.arn}/*"]
        Principal = "*"
      }
    ]
  })
}

# Optionally enable versioning for the bucket
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.existing_bucket.bucket

  versioning_configuration {
    status = "Enabled"
  }
}

# Optionally add lifecycle rules to the bucket
resource "aws_s3_bucket_lifecycle_configuration" "lifecycle_rule" {
  bucket = aws_s3_bucket.existing_bucket.bucket

  rule {
    id     = "expire-logs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    expiration {
      days = 30
    }
  }
}

