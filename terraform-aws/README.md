# Purpose
This Terraform configuration provisions an AWS infrastructure with an Elastic Kubernetes Service (EKS) cluster, configures 
access, and deploys Kubernetes manifests. It creates a security group for traffic management, sets up an EKS cluster with 
a managed node group, and updates the kubeconfig for cluster access. Additionally, it applies Kubernetes manifests from a 
local directory, waits for services to initialize, and retrieves the external IP of a deployed service, outputting it for 
external access.

# Prerequisites
aws CLI (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

kubectl (https://kubernetes.io/docs/tasks/tools/)


# Setup
Navigate to the terraform-aws folder and run the following commands:
```shell
terraform init
```
```shell
terraform apply -target=aws_security_group.my-security-group -auto-approve && terraform apply -auto-approve
```
## Cleanup
For destroying the resources created by terraform run the following command:
```shell
terraform destroy -auto-approve
```

Careful! The terraform script will create one or more AWS load balancers which will not get deleted by the terraform
destroy command. You will need to destroy them with the UI (EC2).