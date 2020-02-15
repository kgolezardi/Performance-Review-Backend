from collections import OrderedDict

from graphene import Field
from graphene.types.base import BaseType
from graphene.types.utils import yank_fields_from_attrs


class Extension(BaseType):
    @classmethod
    def __init_subclass_with_meta__(
            cls,
            **options
    ):
        fields = OrderedDict()

        for base in reversed(cls.__mro__):
            fields.update(yank_fields_from_attrs(base.__dict__, _as=Field))

        base = options['base']

        base._meta.fields.update(fields)

        for name in fields.keys():
            resolver = getattr(cls, "resolve_{}".format(name), None)
            if resolver:
                setattr(base, "resolve_{}".format(name), resolver)

        super(Extension, cls).__init_subclass_with_meta__()
