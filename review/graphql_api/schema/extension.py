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

        for name in fields.keys():
            assert name not in base._meta.fields, "{name} already exists in {base}".format(name=name,
                                                                                           base=base.__name__)

            assert not hasattr(base, "resolve_{}".format(name)), "{base} already has {name} resolver".format(name=name,
                                                                                                             base=base.__name__)
            resolver = getattr(cls, "resolve_{}".format(name), None)
            if resolver:
                setattr(base, "resolve_{}".format(name), resolver)

        base._meta.fields.update(fields)
        super(Extension, cls).__init_subclass_with_meta__()
