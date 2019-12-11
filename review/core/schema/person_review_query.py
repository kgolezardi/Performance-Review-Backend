import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from core.interactors import get_person_review, get_all_person_reviews
from core.schema.enums import Evaluation
from graphql_api.schema.utils import get_node
from ..models import PersonReview


class PersonReviewNode(DjangoObjectType):
    class Meta:
        model = PersonReview
        fields = [
            'reviewee',
            'sahabiness_comment',
            'problem_solving_comment',
            'execution_comment',
            'thought_leadership_comment',
            'leadership_comment',
            'presence_comment',
            'strengths',
            'weaknesses'
        ]
        interfaces = (relay.Node,)

    sahabiness_rating = Evaluation()
    problem_solving_rating = Evaluation()
    execution_rating = Evaluation()
    thought_leadership_rating = Evaluation()
    leadership_rating = Evaluation()
    presence_rating = Evaluation()

    @classmethod
    def base_query_set(cls, info):
        # TODO move this logic to interactor
        if info.context.user.is_authenticated:
            user = info.context.user
            return get_all_person_reviews(user)
        return PersonReview.objects.none()

    @classmethod
    def get_node(cls, info, id):
        try:
            return PersonReviewNode.base_query_set(info).get(id=id)
        except cls._meta.model.DoesNotExist:
            return None


class PersonReviewQuery(graphene.ObjectType):
    person_review = relay.Node.Field(PersonReviewNode)
    person_reviews = graphene.List(graphene.NonNull(PersonReviewNode), required=True)
    find_person_review = graphene.Field(PersonReviewNode, reviewee_id=graphene.ID())

    def resolve_person_reviews(self, info):
        return PersonReviewNode.base_query_set(info)

    def resolve_find_person_review(self, info, reviewee_id):
        reviewee = get_node(reviewee_id, info, User)
        reviewer = info.context.user
        return get_person_review(reviewee=reviewee, reviewer=reviewer)
