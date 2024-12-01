# Generated by Django 5.1.3 on 2024-12-01 00:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('giftcards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('paymentmethodid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('cardnumber', models.CharField(max_length=20)),
                ('expirationdate', models.DateTimeField()),
                ('cvv', models.CharField(max_length=4)),
                ('nameoncard', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False)),
                ('orderdate', models.DateTimeField(auto_now_add=True)),
                ('orderstatus', models.IntegerField(choices=[(1, 'Pending'), (2, 'Processing'), (3, 'Shipped'), (4, 'Completed'), (5, 'Cancelled')], default=1)),
                ('orderTotal', models.FloatField(default=0.0)),
                ('recipient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('itemid', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('giftcardid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcards.giftcard')),
                ('orderid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentid', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=20)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('paymentmethod', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.paymentmethod')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.payment'),
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('cartid', models.AutoField(primary_key=True, serialize=False)),
                ('orderTotal', models.FloatField(default=0.0)),
                ('userid', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('itemid', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('cartid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shoppingcart')),
                ('giftcardid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcards.giftcard')),
            ],
        ),
    ]
