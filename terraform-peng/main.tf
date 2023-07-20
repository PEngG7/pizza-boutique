
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.56.0"
    }
  }
}

provider "google" {
  project     = var.gcp_project_id
  region      = var.region
  zone        = var.zone
}

provider "google-beta" {
  project     = var.gcp_project_id
  region      = var.region
  zone        = var.zone
}

module "enable_google_apis" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 14.0"

  project_id                  = var.gcp_project_id
  disable_services_on_destroy = false

  activate_apis = [
    "container.googleapis.com",
  ]
}

## Create GKE cluster
resource "google_container_cluster" "pizza-boutique" {
  name               = "pizza-boutique"
  location           = var.region
  ip_allocation_policy {}
  node_pool {
    initial_node_count = var.node_count
    node_config {
      image_type = "COS_CONTAINERD"
      machine_type = "n1-standard-8"
      #     service_account = google_service_account.default.email
      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
  }
  depends_on = [
    module.enable_google_apis
  ]
}

module "gcloud" {
  source  = "terraform-google-modules/gcloud/google"
  version = "3.1.2"
  platform = "linux"
  use_tf_google_credentials_env_var = true

  additional_components = ["kubectl", "beta"]
  create_cmd_entrypoint = "gcloud"
  create_cmd_body      = "container clusters get-credentials ${google_container_cluster.pizza-boutique.name} --zone=${var.region} --project=${var.gcp_project_id}"
  module_depends_on = [
    google_container_cluster.pizza-boutique
  ]
}

resource "null_resource" "install_istio" {
  provisioner "local-exec" {
    interpreter = ["bash", "-exc"]
    command = "istioctl install -y"
  }
  depends_on = [
    module.gcloud, google_container_cluster.pizza-boutique
  ]
}

resource "null_resource" "istio_addons" {
  provisioner "local-exec" {
    interpreter = ["bash", "-exc"]
    command = "kubectl apply -f ../istio-manifests/addons/."
  }
  depends_on = [
    module.gcloud, null_resource.install_istio
  ]
}

