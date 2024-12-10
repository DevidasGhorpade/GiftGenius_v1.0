# Generated by Django 5.1.3 on 2024-12-10 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseGiftCard',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False)),
                ('card_number', models.CharField(max_length=50, unique=True)),
                ('cvv', models.CharField(max_length=4)),
                ('balance', models.FloatField()),
                ('gift_message', models.TextField()),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Redeemed'), (4, 'Expired')])),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('update_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='GiftCardType',
            fields=[
                ('card_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('card_name', models.CharField(max_length=100)),
                ('card_description', models.TextField()),
                ('card_category', models.IntegerField(choices=[(1, 'Baby'), (2, 'Birthday'), (3, 'Books'), (4, 'Clothing'), (5, 'Electronics'), (6, 'Entertainment'), (7, 'Fathers Day'), (8, 'Mothers Day'), (9, 'Retail'), (10, 'Travel'), (11, 'Wedding')])),
                ('card_type', models.IntegerField(choices=[(1, 'Digital'), (2, 'Physical')])),
                ('card_quantity', models.PositiveIntegerField()),
                ('card_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cashback', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('vendor', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DigitalGiftCard',
            fields=[
                ('basegiftcard_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='giftcards.basegiftcard')),
                ('delivery_date', models.DateField()),
                ('card_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcards.giftcardtype')),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='digital_giver', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='digital_recipient', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('giftcards.basegiftcard',),
        ),
        migrations.CreateModel(
            name='PhysicalGiftCard',
            fields=[
                ('basegiftcard_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='giftcards.basegiftcard')),
                ('shipping_method', models.IntegerField(choices=[(1, 'US Postal Service'), (2, 'UPS'), (3, 'FedEx'), (4, 'DHL')])),
                ('card_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcards.giftcardtype')),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physical_giver', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physical_recipient', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('giftcards.basegiftcard',),
        ),
    ]
