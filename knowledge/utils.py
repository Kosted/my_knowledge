from django.http import Http404


def get_object(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise Http404


def add_user_to_data(request):
    request.data['user'] = request.user.pk


def chain_filter(model, q_conditions, **kwargs):
    """The chain of applying filters to the model

    :param model: django model from which to search
    :param q_conditions: a list of Q expressions to be applied sequentially to a model
    :param kwargs: key-value to look up before chaining
    """
    if kwargs:
        res = model.objects.filter(**kwargs)
    else:
        res = model.objects.all()

    for q in q_conditions:
        res = res.filter(q)
    return res
