# Generated by Django 5.1.3 on 2024-11-12 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='usertype',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'Customer'), (3, 'Recipient')], default=2),
        ),
    ]
