output "instance_ip" {
  value = aws_instance.api_server.public_ip
}

output "cloudwatch_log_group" {
  value = aws_cloudwatch_log_group.api_logs.name
}