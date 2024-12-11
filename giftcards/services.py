from .models import GiftCardType, BaseGiftCard
from django.db.models import Q

class GiftCardCatalog:
    def search_gift_card_type(self, name):
        return GiftCardType.objects.filter(card_name__icontains=name)

    def filter_gift_card_types_by_amount(self, min_amount, max_amount):
        return GiftCardType.objects.filter(amount__gte=min_amount, amount__lte=max_amount)

    def get_gift_card_type_by_id(self, gift_card_type_id):
        try:
            return GiftCardType.objects.get(card_id=gift_card_type_id)
        except GiftCardType.DoesNotExist:
            return None

    def get_gift_cards_by_status(self, status):
        return BaseGiftCard.objects.filter(status=status)


class SearchEngine:
    def __init__(self):
        self.search_results = None

    def perform_search(self, query):
        self.search_results = GiftCardType.objects.filter(
            Q(card_name__icontains=query) | Q(card_description__icontains=query)
        )
        return self.search_results

    def sort_results(self, criteria, queryset=None):
        if queryset is None:
            queryset = self.search_results or GiftCardType.objects.all()

        sort_fields = {
            "price": "amount",
            "availability": "card_quantity",
            "vendor": "vendor",
            "cashback": "cashback"
        }

        match criteria:
            case "price" | "availability" | "vendor" | "cashback":
                sort_field = sort_fields[criteria]
            case _:
                sort_field = None

        if sort_field:
            queryset = queryset.order_by(sort_field)
        else:
            queryset = self.search_results

        return queryset
