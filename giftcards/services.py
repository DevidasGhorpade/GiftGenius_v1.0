from .models import GiftCard
from django.db.models import Q

class GiftCardCatalog:
    def search_gift_card(self, name):
        return GiftCard.objects.filter(card_name__icontains=name)

    def filter_gift_cards_by_amount(self, min_amount, max_amount):
        return GiftCard.objects.filter(amount__gte=min_amount, amount__lte=max_amount)

    def get_gift_card_by_id(self, gift_card_id):
        try:
            return GiftCard.objects.get(card_id=gift_card_id)
        except GiftCard.DoesNotExist:
            return None

class SearchEngine:
    def __init__(self):
        self.search_results = []

    def perform_search(self, query):
        self.search_results = GiftCard.objects.filter(
            Q(card_name__icontains=query) | Q(card_description__icontains=query)
        )
        return self.search_results

    def sort_results(self, criteria):
        if criteria == "price":
            return self.search_results.order_by("amount")
        elif criteria == "availability":
            return self.search_results.order_by("balance")
        return self.search_results