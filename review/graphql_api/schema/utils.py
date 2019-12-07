from graphene import relay


def get_node(global_id, info, model=None):
    obj = relay.Node.get_node_from_global_id(global_id=global_id, info=info)
    if model and not isinstance(obj, model):
        return None
    return obj
