from django.shortcuts import render

from giftcards.models import GiftCardType
from .services import GiftCardCatalog, SearchEngine
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def giftcard_list(request):
    catalog = GiftCardCatalog()
    search_engine = SearchEngine()

    query = request.GET.get('search', '')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    sort_criteria = request.GET.get('sort')

    if query:
        giftcards = search_engine.perform_search(query)
    elif min_amount and max_amount:
        giftcards = catalog.filter_gift_card_types_by_amount(float(min_amount), float(max_amount))
    else:
        giftcards = catalog.search_gift_card_type('')

    if sort_criteria:
        giftcards = search_engine.sort_results(sort_criteria)

    return render(request, 'giftcards/giftcard_list.html', {'giftcards': giftcards})

def giftcard_detail(request, card_type_id):
    try:
        giftcard = GiftCardType.objects.get(card_type_id=card_type_id)
    except GiftCardType.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'giftcards/giftcard_details.html', {'giftcard': giftcard})
