from typing import Collection


def cslist(items: Collection = None,  conjunction='and', *, use_oxford_comma=True, sepr: str = ', ',):
    if items is None:
        items = tuple()
    elif not isinstance(items, Collection):
        items = (items, )

    # a, b, and c

    # Handle single item by returning the item
    if 1 == len(items):
        return ''.join([str(item) for item in items])

    if use_oxford_comma and 2 < len(items):
        conjucntion_str = f', {conjunction} '
    else:
        conjucntion_str = f' {conjunction} '

    return conjucntion_str.join((sepr.join(items[0:-1]), items[-1]))
