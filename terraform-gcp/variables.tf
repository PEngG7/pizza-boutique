# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
variable "gcp_project_id" {
  type        = string
  description = "The GCP project ID to apply this config to"
}

variable "name" {
  type        = string
  description = "Name given to the new GKE cluster"
  default     = "sock-shop"
}

variable "region" {
  type        = string
  description = "Region of the new GKE cluster"
  default     = "us-east1"
}

variable "zone" {
  type        = string
  description = "Region of the new GKE cluster"
  default     = "us-east1-c"
}

variable "namespace_istio" {
  type        = string
  description = "Kubernetes Namespace in which the Istio resources are to be deployed"
  default     = "istio-system"
}

variable "node_count" {
  description = "Number of nodes (VMs) after creating the container"
  type        = number
  default = 1
}