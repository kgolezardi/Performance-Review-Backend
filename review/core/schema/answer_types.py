import graphene
from graphene_django import DjangoObjectType

from core.models import Answer
from core.schema.question_node import QuestionNode
from graphql_api.schema.utils import get_node_global_id


class AnswerOutput(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ['value']

    question_id = graphene.NonNull(graphene.ID)

    def resolve_question_id(self, info):
        return get_node_global_id(QuestionNode, self.question.id)


class AnswerInput(graphene.InputObjectType):
    question_id = graphene.NonNull(graphene.ID)
    value = graphene.String()
