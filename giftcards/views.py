from django.shortcuts import redirect, render

from giftcards.models import GiftCardCategory, GiftCardType
from .services import GiftCardCatalog, SearchEngine
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def giftcard_list(request):
    if not request.user.preferred_category:
        giftcard_categories = [(choice.value, choice.label) for choice in GiftCardCategory]
        return render(request, 'giftcards/set_preference.html', {
            'giftcard_categories': giftcard_categories,
        })

    preferred_category = request.user.preferred_category
    search_engine = SearchEngine()

    query = request.GET.get('search', '')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    sort_criteria = request.GET.get('sort')

    if query:
        search_results = search_engine.perform_search(query)
    else:
        search_results = GiftCardType.objects.all()

    if min_amount and max_amount:
        search_results = search_results.filter(amount__gte=min_amount, amount__lte=max_amount)

    preferred_cards = search_results.filter(card_category=preferred_category)
    other_cards = search_results.exclude(card_category=preferred_category)

    if sort_criteria:
        preferred_cards = search_engine.sort_results(sort_criteria, preferred_cards)
        other_cards = search_engine.sort_results(sort_criteria, other_cards)

    return render(request, 'giftcards/giftcard_list.html', {
        'preferred_cards': preferred_cards,
        'other_cards': other_cards,
    })

def giftcard_detail(request, card_type_id):
    try:
        giftcard = GiftCardType.objects.get(card_type_id=card_type_id)
    except GiftCardType.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'giftcards/giftcard_details.html', {'giftcard': giftcard})

@login_required(login_url='login')
def set_preferred_category(request):
    if request.method == 'POST':
        if preferred_category := request.POST.get('preferred_category'):
            request.user.preferred_category = preferred_category
            request.user.save()
            return redirect('giftcard_list')

    return redirect('giftcard_list')
