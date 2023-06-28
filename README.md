# Run
```
minikube start --driver=docker
```
```
kubectl apply -f ./release/kubernetes-manifests.yaml
```
```
kubectl get pods
```
```
kubectl port-forward deployment/frontend 8080:8080
```
Open ```http://localhost:8080```
