# Pipeline Wrapper
Abstraction for invoking a Python-based ML model using the inputs and outputs provided by a configured **Parameter Server**.

## Setup
* Install Ray library:
```
pip install -r  requirements.txt
```

* Deploy Ray cluster:
```
kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"
kubectl create ns ray
kubectl apply -f resources/ray-cluster.yaml -n ray
watch kubectl get pods --selector=ray.io/cluster=raycluster-autoscaler -nray
source .env
# envsubst < resources/ray-cluster-http-proxy.in.yaml > resources/ray-cluster-http-proxy.yaml
# kubectl apply -f resources/ray-cluster-http-proxy.yaml
RAY_HEAD_POD=$(kubectl get pod -o name -l ray.io/node-type=head -nray)
kubectl expose svc raycluster-autoscaler-head-svc --type LoadBalancer --port 8265 --target-port 8265 --name raycluster-svc -n ray
kubectl expose pod $RAY_HEAD_POD --type LoadBalancer --port 10001 --target-port 10001 --name raycluster-head-svc -n ray
```

* Deploy the Gemfire operator (only required if it is not already installed on the cluster):
```
export GEM_OPERATOR_VERSION=1.0.3
export 
kubectl create ns gemfire-system --dry-run -o yaml | kubectl apply -f -
kubectl create secret docker-registry image-pull-secret --namespace=gemfire-system --docker-server=registry.pivotal.io --docker-username='{{ DATA_E2E_PIVOTAL_REGISTRY_USERNAME }}' --docker-password='{{ DATA_E2E_PIVOTAL_REGISTRY_PASSWORD }}' --dry-run -o yaml | kubectl apply -f -
helm uninstall  gemfire --namespace gemfire-system || true
helm install gemfire other/resources/gemfire/gemfire-operator-${GEM_OPERATOR_VERSION}/ --namespace gemfire-system
```

* Deploy Gemfire cluster:
```
kubectl apply -f resources/gemfire-cluster.yaml -n gemfire-system
```
