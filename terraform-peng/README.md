# Evaluation setup with Terraform and GCP

To simplify the setup of our experiments, we provide Terraform files.

## Prerequirements
•	The Terraform cli needs to be installed (https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

•	Authentication to your GCP project either through this command
```shell
gcloud auth application-default login
``` 
or by Providing a service account json as an environment variable (run it in the dir with the json file):
```shell
export GOOGLE_CREDENTIALS="$(cat <<your_json_file>>)"
``` 
or any other method.

## Start

First of all export your GCP project ID:
```shell
export GCP_PROJECT_ID=<<your-project-id>>
```
Then run the following command to apply your project-id:
```shell
awk -v new_value="$GCP_PROJECT_ID" '/gcp_project_id/ {sub(/"peng-392207"/, "\"" new_value "\"")} 1' ./terraform/terraform.tfvars > temp.tfvars && mv temp.tfvars ./terraform/terraform.tfvars
```
or set the gcp_project_id in the terraform.tfvars manually.

The provided Terraform files can now be used to create your Kubernetes cluster in your GCP project.

Navigate to the terraform-peng folder (cd terraform-peng) and run the following commands:
```shell
terraform init
```
```shell
terraform apply
```
Check the plan and if it is according to expectations type "yes" and enter.

Now your cluster will be created which can take a couple of minutes.

The cluster has the following settings:
•	Location: us-central1-c

•	Number of nodes: 3

•	Total vCPUs: 24

•	Total memory: 90GB


•	Location type: Zonal

•	Machine type: n1-standard-8

We are using Istio for an easy Pronetheus/Grafana integration but intentionally do not label the namespace. Consequently,
the Envoy proxies are not added as a sidecar to the services. We do not need the telementry provided by Envoy since we 
exposed our own custom metrics to Prometheus.

Having set up the cluster, we can now measure the latency and throughput.

## Evaluation
After the cluster and all it's components are fully deployed, we can start taking measurements. Each of our measurements were done over a period of 10 minutes.
We are measuring the performance of our purposelimiter component while it is deployed as part of a pizza boutique in the Google Cloud.
A measurement is started by deploying and running the pizza boutique, which is done with the following command:
```shell
skaffold run --default-repo=gcr.io/[PROJECT_ID]
```
In our case the project id was 'peng-392207'.
We measure the performance of our purposelimiter component directly by having created custom prometheus metrics that observe the duration of an request ('grpc_request_milliseconds_summary') going through the interceptor as well as the number of attempted ('grpc_request_sent') and completed requests ('requests_success_total').
These metrics can be accessed via the prometheus interface by running the following command:
```shell
kubectl port-forward deploy/prometheus -n istio-system 9090:9090
```
Accessing localhost:9090 then allows you to look at all predfined prometheus and isteo metrics as well as our custom made metrics.

Our test cases can be divided into different scenarios, which are different message sizes (meaning the numbert of fields in a request/response) and different purposes given for a service, which allows or restricts the access to personal information based on our minimization techniques.
Depending on which scenarios is tested, modifications have to be made to the source code of either the tracking service or the loadgenerator.
In order to test different purposes of a policy the following lines of the locust.py in the loadgenerator have to be adjusted:
Line 79 to 89 define different access tokens for our predefined policies. Only one of these tokens is needed for a specific purpose. Comment or uncomment the wanted token. This step has to be repeated everytime a different purpose is tested. 
It's important to note that the tokens in the locustfile might have expired by the time these steps are reproduced and require a new generation of tokens for each policy.

Additional modifications are required in case different message sizes want to be tested.
The files in the genproto folder of the trackingservice have to be replaced with either the files inside the folder 'genproto_26fields' or the files inside 'genproto_52fields'.
In the main.go file of the trackingservice lines 148 to 160 have to be uncommented in case you want to test with 26 fields in a message or lines 148 to 186 have to be uncommented for 52 fields.
In the locust.py file of the loadgenerator the imports between lines 6 to 16 have to be adjusted depending on which message size is supposed to be tested.
And lines 119 to 127 of the same locust.py have to be uncommented for messages with 26 fields or 119 to 157 for messages with 52 fields.

The last adjustment that can be done is between the different kind of interceptors which are no interceptor at all, a no-op interceptor, our own interceptor and the naive monolithic approach. The distinction is made in the lines 95 to 118 in the main.go file of the trackingservice.
Each change to the source code requires the redeployment of our boutique, which is again done with:
```shell
skaffold run --default-repo=gcr.io/[PROJECT_ID]
```

## Cleanup
After you are done with everything use the following command to shut the cluster down.
```shell
terraform destroy
```