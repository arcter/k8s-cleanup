# Cleanup

A simple python script to delete and scale down any object in Kubernetes that can prevent Terraform to delete all resources that are part of Kubernetes. This may include Ingresses that create ALBs inside AWS, PVCs that are creating extra attached volumes on the nodes or CRDs that can get "stuck".

Please use it carefully as it pretty much designed to start dismantling your cluster.