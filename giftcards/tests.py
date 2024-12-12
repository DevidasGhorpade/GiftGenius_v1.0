from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import GiftCardCategory, CardType, GiftCardType, GiftCardStatus


class GiftCardTypeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="phoenix",
            email="phoenix@example.local",
            password="TestPass1342!",
            preferred_category=6,
        )
        cls.giftcard1 = GiftCardType.objects.create(
            card_name="Spotify Gift Card",
            card_description="A gift card to enjoy Spotify Premium.",
            card_category=6,
            card_type=1,
            card_quantity=50,
            card_image_url="https://pisces.bbystatic.com/image2/BestBuy_US/images/products/2800/2800086_sd.jpg;maxHeight=640;maxWidth=550;format=webp",
            amount="200.00",
            cashback="10.00",
            vendor="Spotify",
            creation_date="2024-01-05T12:00:00Z",
            update_date="2024-01-20T12:00:00Z",
        )
        cls.giftcard2 = GiftCardType.objects.create(
            card_name="Best Buy Gift Card",
            card_description="A gift card for electronics and gadgets at Best Buy.",
            card_category=9,
            card_type=2,
            card_quantity=30,
            card_image_url="https://m.media-amazon.com/images/I/31rakPi6KsL._SY400_.jpg",
            amount="100.00",
            cashback="5.00",
            vendor="Best Buy",
            creation_date="2024-01-10T15:00:00Z",
            update_date="2024-01-25T15:00:00Z",
        )

    def test_giftcard_listing(self):
        self.assertEqual(f"{self.giftcard1.card_name}", "Spotify Gift Card")
        self.assertEqual(f"{self.giftcard1.card_type}", "1")
        self.assertEqual(f"{self.giftcard1.amount}", "200.00")

        self.assertEqual(f"{self.giftcard2.card_name}", "Best Buy Gift Card")
        self.assertEqual(f"{self.giftcard2.card_type}", "2")
        self.assertEqual(f"{self.giftcard2.amount}", "100.00")

    def test_giftcard_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("giftcard_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spotify Gift Card")
        self.assertContains(response, "Best Buy Gift Card")
        self.assertTemplateUsed(response, "giftcards/giftcard_list.html")

    def test_giftcard1_detail_view(self):
        response = self.client.get(reverse("giftcard_detail", args="1"))
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Spotify Gift Card")
        self.assertTemplateUsed(response, "giftcards/giftcard_details.html")

    def test_giftcard2_detail_view(self):
        response = self.client.get(reverse("giftcard_detail", args="2"))
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Best Buy Gift Card")
        self.assertTemplateUsed(response, "giftcards/giftcard_details.html")
