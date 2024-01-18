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