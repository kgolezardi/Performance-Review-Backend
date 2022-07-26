from graphene import relay
from graphene_django import DjangoObjectType

from core.models import Question
from core.schema.enums import QuestionType


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        fields = [
            'label',
            'order',
            'choices',
            'max_choices',
            'help_text',
            'private_answer_to_peer_reviewers',
            'private_answer_to_reviewee',
        ]
        interfaces = (relay.Node,)

    question_type = QuestionType(required=True)
