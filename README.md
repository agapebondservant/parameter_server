# Pipeline Wrapper
Abstraction for invoking a Python-based ML model using the inputs and outputs provided by a configured **Parameter Server**.

## Setup
* Install Ray library:
``` 
pip install -r  requirements.txt
OR
/usr/bin/python -m pip install -r requirements.txt (might be necessary for some Macs)
```

* Deploy Ray cluster:
```
kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"
kubectl create ns ray
kubectl apply -f resources/ray-cluster.yaml -n ray
watch kubectl get pods --selector=ray.io/cluster=raycluster-autoscaler -nray
export RAY_HEAD_POD=$(kubectl get pod -o name -l ray.io/node-type=head -nray)
kubectl expose svc raycluster-autoscaler-head-svc --port 8265 --target-port 8265 --name raycluster-svc -n ray
kubectl expose $RAY_HEAD_POD --type LoadBalancer --port 10001 --target-port 10001 --name raycluster-head-svc -n ray
export RAY_BASE_URL=tanzudatadev.ml
envsubst < resources/ray-cluster-http-proxy.in.yaml > resources/ray-cluster-http-proxy.yaml
kubectl apply -f resources/ray-cluster-http-proxy.yaml
```

* To undeploy Ray cluster:
```
kubectl delete -f resources/ray-cluster.yaml -n ray
kubectl delete ns ray
kubectl delete -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"
```

* Deploy the Gemfire operator (only required if it is not already installed on the cluster):
```
export GEM_OPERATOR_VERSION=1.0.3
export PIVOTAL_USERNAME=<your pivotal username>
export PIVOTAL_PASSWORD=<your pivotal password>
export REGISTRY_USERNAME=<your registry username>
export REGISTRY_PASSWORD=<your registry password>
kubectl create ns gemfire-system --dry-run -o yaml | kubectl apply -f -
kubectl create secret docker-registry image-pull-secret --namespace=gemfire-system --docker-server=registry.pivotal.io --docker-username='${PIVOTAL_USERNAME}' --docker-password='${PIVOTAL_PASSWORD}' --dry-run -o yaml | kubectl apply -f -
kubectl create secret docker-registry reg-image-pull-secret --namespace=gemfire-system --docker-server=registry.pivotal.io --docker-username='${REGISTRY_USERNAME}' --docker-password='${REGISTRY_PASSWORD}' --dry-run -o yaml | kubectl apply -f -
helm uninstall  gemfire --namespace gemfire-system || true
helm install gemfire other/resources/gemfire/gemfire-operator-${GEM_OPERATOR_VERSION}/ --namespace gemfire-system
```

* Deploy Gemfire cluster:
```
kubectl apply -f resources/gemfire-cluster.yaml -n gemfire-system
```

* Create Gemfire region:
```

```
