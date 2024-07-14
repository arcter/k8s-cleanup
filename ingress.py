import kubernetes.client

def get_ingresses(api_client):
    res=[]
    api_instance = kubernetes.client.NetworkingV1Api(api_client)
    api_response = api_instance.list_ingress_for_all_namespaces()
    for item in api_response.items:
        res.append([item.metadata.name,item.metadata.namespace])
    return res
ingress__deletionstring="Ingress {name}is deleted in namespace {namespace}"

def delete_all_ingress(api_client):
    ingresses=get_ingresses(api_client)
    for ingress in ingresses:
        delete_ingress(api_client=api_client,ingress_name=ingress[0],ingress_namespce=ingress[1])

def delete_ingress(api_client,ingress_name,ingress_namespce):
    api_instance = kubernetes.client.NetworkingV1Api(api_client)
    api_instance.delete_namespaced_ingress(name=ingress_name, namespace=ingress_namespce)
    print(ingress__deletionstring.format(name=ingress_name,namespace=ingress_namespce))