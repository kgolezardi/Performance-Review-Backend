def filter_query_set_for_manager_review(viewer, query_set, reviewee_field=None):
    if viewer.is_hr:
        return query_set
    manager_field = '%s__manager' % reviewee_field if reviewee_field else 'manager'
    return query_set.filter(**{manager_field: viewer})
