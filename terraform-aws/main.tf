
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    flux = {
      source = "fluxcd/flux"
    }
    github = {
      source  = "integrations/github"
      version = ">=5.18.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

resource "aws_security_group" "my-security-group" {
  name        = "my-security-group"
  description = "Allow inbound all TCP traffic and outbound all traffic"

  ingress {
    from_port = 0
    to_port   = 65535
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  vpc_id = "vpc-0f2d9adf03961f221"
  subnet_ids      = ["subnet-028b97041fb0039d2", "subnet-0692049a797200744", "subnet-08caccd9e5f668d89"]
  cluster_endpoint_public_access = true

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"
    instance_types = ["t3.large"]
  }

  eks_managed_node_groups = {
    one = {
      name = "default"

      instance_types = ["t3.large"]
      min_size     = 1
      max_size     = 4
      desired_size = 2

      vpc_security_group_ids = [aws_security_group.my-security-group.id]
    }
  }
  depends_on = [aws_security_group.my-security-group]
}

resource "terraform_data" "fetch_aws_endpoint" {
  provisioner "local-exec" {
    interpreter = ["bash", "-exc"]
    command = "aws eks update-kubeconfig --name ${var.cluster_name} --region eu-central-1"
  }
  depends_on = [module.eks]
}

resource "terraform_data" "apply_manifests" {
  provisioner "local-exec" {
    interpreter = ["bash", "-exc"]
    command = "kubectl apply -k ../kubernetes-manifests-aws/"
  }
  depends_on = [terraform_data.fetch_aws_endpoint]
}

# Waiting time to let service get ready
resource "terraform_data" "wait" {
  provisioner "local-exec" {
    command = "sleep 30"
  }
  depends_on = [terraform_data.apply_manifests]
}


data "external" "external_ip" {
  program = ["bash", "-c", "kubectl get svc frontend-external -o json | jq -n '{ gateway_ip: input.status.loadBalancer.ingress[0].hostname }'"]
  depends_on = [terraform_data.apply_manifests]
}

output "gateway_ip" {
  value = data.external.external_ip.result.gateway_ip
  depends_on = [data.external.external_ip]
}
