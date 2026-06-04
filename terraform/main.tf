provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

data "aws_security_group" "existing_sg" {
  name = "fraud-detection-sg"
}

resource "aws_instance" "api_server" {
  ami                    = "ami-000752eb6598fea3c"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [data.aws_security_group.existing_sg.id]

  tags = {
    Name = "cicd-pipeline-api"
  }

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    service docker start
    docker run -d -p 8000:8000 --name cicd-api python:3.11-slim python3 -c "
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
    HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
    "
  EOF
}

resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/cicd-pipeline/api"
  retention_in_days = 7
}

resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "cicd-pipeline-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "CPU utilization exceeded 80%"

  dimensions = {
    InstanceId = aws_instance.api_server.id
  }
}