# Generated by Django 4.1.2 on 2022-10-31 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_listings_category_listings_description_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bids",
            name="bid_value",
        ),
        migrations.RemoveField(
            model_name="bids",
            name="bid_value_currency",
        ),
        migrations.RemoveField(
            model_name="listings",
            name="current_price",
        ),
        migrations.RemoveField(
            model_name="listings",
            name="current_price_currency",
        ),
        migrations.RemoveField(
            model_name="listings",
            name="start_price",
        ),
        migrations.RemoveField(
            model_name="listings",
            name="start_price_currency",
        ),
        migrations.RemoveField(
            model_name="user",
            name="balance",
        ),
        migrations.RemoveField(
            model_name="user",
            name="balance_currency",
        ),
    ]
