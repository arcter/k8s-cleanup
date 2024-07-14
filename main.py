from pick import pick  # install pick using `pip install pick`
import kubernetes
from kubernetes import client, config
from ingress import delete_all_ingress
from pod_managers.deployments import scale_down_all_deployments
from pod_managers.daemonset import get_daemonsets, delete_all_daemonsets
ingress_string="Name is {name}, namespace is {namespace}"
deployment_string="Name is {name}, namespace is {namespace}"
daemonset_string="Name is {name}, namespace is {namespace}"

def select_cluster():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])
    cluster, index = pick(contexts, title="Pick the  context",
                                 default_index=active_index)
    return cluster

def select_namespace(api_client):
    k8s_client = client.CoreV1Api(
        api_client=api_client)
    namespaces=[]
    q="Select the namespace to spare"
    for n in k8s_client.list_namespace().items:
        namespaces.append(n.metadata.name)
    ns=pick(namespaces,q,multiselect=True,min_selection_count=0)
    res=[]
    for n in ns:
        res.append(n[0])
    return res

def main():
    cluster=select_cluster()
    api_client=config.new_client_from_config(context=cluster)
    ns=select_namespace(api_client)
    if ns== []:
        print("No namespace selected")
    else:
        for n in ns:
            print(n)

    # delete_all_ingress(api_client=api_client)
    # scale_down_all_deployments(api_client=api_client,exceptions_namespaces=ns)
    daemonsets=get_daemonsets(api_client)
    for d in daemonsets:
        print(daemonset_string.format(name=d[0],namespace=d[1]))
    delete_all_daemonsets(api_client=api_client,exceptions_namespaces=ns)
if __name__ == '__main__':
    main()