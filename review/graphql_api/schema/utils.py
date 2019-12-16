from graphene import relay
from graphql_relay import to_global_id


def get_node(global_id, info, model=None):
    obj = relay.Node.get_node_from_global_id(global_id=global_id, info=info)
    if model and not isinstance(obj, model):
        return None
    return obj


def get_node_global_id(node, id):
    if id is None:
        return None
    return to_global_id(node.__name__, id)
