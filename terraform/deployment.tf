resource "kubernetes_deployment" "terraform_demo" {
  metadata {
    name = "terraform-demo"

    labels = {
      app = "terraform-demo"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "terraform-demo"
      }
    }

    template {
      metadata {
        labels = {
          app = "terraform-demo"
        }
      }

      spec {
        container {
          name  = "nginx"
          image = "nginx:alpine"

          port {
            container_port = 80
          }

          resources {
            requests = {
              cpu    = "50m"
              memory = "64Mi"
            }
            limits = {
              cpu    = "100m"
              memory = "128Mi"
            }
          }
        }
      }
    }
  }
}

