import kubernetes.client


def get_deployments(api_client):
    res=[]
    api_instance = kubernetes.client.AppsV1Api(api_client)
    api_response = api_instance.list_deployment_for_all_namespaces()
    for item in api_response.items:
        res.append([item.metadata.name,item.metadata.namespace])
    return res

deployment_scalingstring="Deployment {name}is scaled to 0 in namespace {namespace}"

def scale_down_all_deployments(api_client,exceptions_namespaces):
    deploymentes=get_deployments(api_client)
    for deployment in deploymentes:
        if deployment[1] not in exceptions_namespaces:
            scale_deployment(api_client=api_client,deployment_name=deployment[0],deployment_namespce=deployment[1])

def scale_deployment(api_client,deployment_name,deployment_namespce):
    api_instance = kubernetes.client.AppsV1Api(api_client)
    api_instance.patch_namespaced_deployment_scale(deployment_name, deployment_namespce, {'spec': {'replicas': 0}})
    print(deployment_scalingstring.format(name=deployment_name,namespace=deployment_namespce))

