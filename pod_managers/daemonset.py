import kubernetes.client


def get_daemonsets(api_client):
    res=[]
    api_instance = kubernetes.client.AppsV1Api(api_client)
    api_response = api_instance.list_daemon_set_for_all_namespaces()
    for item in api_response.items:
        res.append([item.metadata.name,item.metadata.namespace])
    return res

daemonset_scalingstring="daemonset {name}is deleted in namespace {namespace}"

def delete_all_daemonsets(api_client,exceptions_namespaces):
    daemonsetes=get_daemonsets(api_client)
    for daemonset in daemonsetes:
        if daemonset[1] not in exceptions_namespaces:
            delete_daemonset(api_client=api_client,daemonset_name=daemonset[0],daemonset_namespce=daemonset[1])

def delete_daemonset(api_client,daemonset_name,daemonset_namespce):
    api_instance = kubernetes.client.AppsV1Api(api_client)
    api_instance.delete_namespaced_daemon_set(daemonset_name, daemonset_namespce)
    print(daemonset_scalingstring.format(name=daemonset_name,namespace=daemonset_namespce))

