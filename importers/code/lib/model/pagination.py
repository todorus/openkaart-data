import math


def paginate(count, **kwargs):
    page = 1
    limit = 10

    if 'limit' in kwargs and kwargs["limit"] > 0:
        limit = kwargs["limit"]
    if 'page' in kwargs and kwargs["page"] > 0:
        page = kwargs["page"]

    if count > 0:
        total = math.ceil(count / float(limit))
    else:
        total = 1

    return {"current": page, "total": total}
