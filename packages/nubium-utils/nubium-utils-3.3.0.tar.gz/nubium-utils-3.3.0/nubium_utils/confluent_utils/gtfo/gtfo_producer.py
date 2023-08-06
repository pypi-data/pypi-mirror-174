from fluvii.auth import SaslPlainClientConfig
from fluvii.producer import Producer
from fluvii.schema_registry import SchemaRegistry
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.yaml_parser import load_yaml_fp


def gtfo_producer(topic_schema_dict):
    cluster_config = load_yaml_fp(env_vars()['NU_KAFKA_CLUSTERS_CONFIGS_YAML'])[load_yaml_fp(env_vars()['NU_TOPIC_CONFIGS_YAML'])[list(topic_schema_dict.keys())[0]]['cluster']]
    auth = SaslPlainClientConfig(username=cluster_config['username'], password=cluster_config['password'])

    return Producer(
        cluster_config['url'],
        schema_registry=SchemaRegistry(env_vars()['NU_SCHEMA_REGISTRY_URL'], auth_config=auth),
        client_auth_config=auth,
        topic_schema_dict=topic_schema_dict,
    )
