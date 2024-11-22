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

    return render(request, 'giftcard/giftcard_list.html', {'giftcards': giftcards})