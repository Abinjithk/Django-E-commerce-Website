from . models import *
from . views import *

def count(request):
    item_count = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            ct = CartList.objects.filter(cart_id=ct_id(request))
            ct_items = Item.objects.all().filter(cart=ct[:1])

            for c in ct_items:
                item_count += c.quantity

        except CartList.DoesNotExist:
            item_count=0

        return dict(item_count=item_count)