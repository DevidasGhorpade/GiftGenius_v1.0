# Generated by Django 5.1.3 on 2024-11-13 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giftcards', '0003_giftcard_card_number_giftcard_card_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='card_number',
            field=models.CharField(max_length=50),
        ),
    ]
