import json
import os
from kubernetes import client, config, watch
import requests

DOMAIN = "api.service.local"
HOOK_TARGET = os.getenv('WEBHOOK_TARGET', 'http://localhost:8080/api/')
HOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'lksdafhlkdjlkjkadsfjkjklj')


def review_item(crds, obj):
    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["review"] = True

    print("Found unreview item: %s" % obj)
    ###r = requests.post('https://httpbin.org/post', data = {'key':'value'})
    ### headers = {'X_API_KEY': ''}
    ### if r.status_code == requests.codes.ok
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "tests", name, obj)


if __name__ == "__main__":
    config.load_incluster_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)
    current_crds = [x['spec']['names']['kind'].lower() for x in v1.list_custom_resource_definition().to_dict()['items']]
    print(current_crds)
    crds = client.CustomObjectsApi(api_client)

    print("Waiting for Items...")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "tests", resource_version=resource_version)
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            if not spec:
                continue
            metadata = obj.get("metadata")
            generation=metadata['generation']
            namespace=metadata['namespace']
            resource_version = metadata['resourceVersion']
            name = metadata['name']
            print("Handling %s event on %s generation %s in namespace %s" % (operation, name, generation, namespace))
            done = spec.get("review", False)
            if done:
                continue
            review_item(crds, obj)
