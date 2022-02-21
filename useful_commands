# Get into container bash
kubectl exec --stdin --tty postgres-5f676c995d-n9lwl -- /bin/sh

# Remove unused replicasets
kubectl delete $(kubectl get all | grep replicaset.apps | grep "0         0         0" | cut -d' ' -f 1)

# Restart deployments
kubectl rollout restart deployment udaconnect-api 