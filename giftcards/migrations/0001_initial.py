# Generated by Django 5.1.3 on 2024-12-01 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCardType',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False)),
                ('card_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('card_description', models.TextField()),
                ('category', models.CharField(choices=[('BIRTHDAY', 'Birthday'), ('TRAVEL', 'Travel'), ('CLOTHING', 'Clothing'), ('BOOKS', 'Books'), ('RETAIL', 'Retail'), ('ENTERTAINMENT', 'Entertainment')], max_length=50)),
                ('type', models.CharField(choices=[('PHYSICAL', 'Physical'), ('DIGITAL', 'Digital')], max_length=20)),
                ('quantity', models.PositiveIntegerField()),
                ('gift_card_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GiftCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('cvv_number', models.CharField(max_length=10)),
                ('gift_card_status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('EXPIRED', 'Expired')], max_length=20)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift_cards', to='giftcards.giftcardtype')),
            ],
        ),
    ]
