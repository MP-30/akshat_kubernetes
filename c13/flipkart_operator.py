import kopf
from kubernetes import client, config

config.load_kube_config()

@kopf.on.create('flipkart.com', 'v1', 'flipkartapplications')
def create_app(spec, name, namespace, **kwargs):

    image = spec.get('image', 'nginx')
    replicas = spec.get('replicas', 1)

    apps_api = client.AppsV1Api()

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": name
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": name
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "app",
                            "image": image
                        }
                    ]
                }
            }
        }
    }

    apps_api.create_namespaced_deployment(
        namespace=namespace,
        body=deployment
    )

    print(f"Deployment {name} created")
